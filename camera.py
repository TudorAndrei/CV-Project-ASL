import time
import re
import collections
import datetime

import cv2
import torch

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (255, 245, 67)
IMG_SIZE = 320
CAMERA_INDEX = 0
CONF_TRESHOLD = 0.3
FONT = cv2.FONT_HERSHEY_SIMPLEX

letter = 0
confs = 0

output_string = []
last_characters = collections.deque()
now = 0
timestamp = 0
string_to_process = []


def get_one_letter(confs, letters):
    if confs:
        max_value_per_confs = max(confs)
        max_index = confs.index(max_value_per_confs)
        letters = letters[max_index]
        confs = confs[max_index]
    return confs, letters


def get_time(letter):
    global last_characters, timestamp
    now = datetime.datetime.now()
    timestamp = int(round(now.timestamp()))
    last_characters.append([timestamp, letter])
    print(last_characters)
    return last_characters


def create_dic(the_list):
    dic = {x: the_list.count(x) for x in the_list}
    return dic


def get_necessary_letter(the_dic):
    max_key = max(the_dic, key=the_dic.get)
    return max_key


def process_time():
    global timestamp, last_characters, output_string
    if (timestamp - last_characters[0][0]) >= 3:
        for i in range(len(last_characters)):
            if last_characters[i][1]:
                string_to_process.append(last_characters[i][1])
        last_characters.clear()
    if string_to_process:
        dic = create_dic(string_to_process)
        letter = get_necessary_letter(dic)
        string_to_process.clear()
        # print((dic[letter] * 100) / sum(dic.values()))
        if (dic[letter] * 100) / sum(dic.values()) >= 90:
            if output_string:
                if output_string[-1] != letter:
                    output_string.append(letter)
                    # print(output_string)
            else:
                output_string.append(letter)
    print(output_string)


def process(confs, letters):
    global output_string
    _, letters_ = get_one_letter(confs, letters)
    get_time(letters_)
    process_time()


class VideoCamera(object):
    def __init__(self):
        try:
            self.video = cv2.VideoCapture(CAMERA_INDEX)
        except:
            print("Camera not initialized")
        sample_rate = 10
        fps = round(self.video.get(cv2.CAP_PROP_FPS))
        self.hop = round(fps / sample_rate)

        self.model = torch.hub.load(
            "yolo",
            "custom",
            path="models/exp20/best.pt",
            source="local",
        )

        self.model.conf = CONF_TRESHOLD
        self.seq = []
        self.font = FONT
        self.font_size = 1.1
        self.font_color = WHITE
        self.font_background = BLACK
        self.font_thickness = 2
        self.prection = ""
        self.buffer = collections.deque([" "] * 20)

    def draw_text(self, frame, name, x, y, conf=None, font_color=None):
        if font_color is None:
            font_color = self.font_color
        if conf:
            text = f"{name} {100*conf:.0f}%"
        else:
            text = str(name)

        (text_w, text_h), _ = cv2.getTextSize(
            text, self.font, self.font_size, self.font_thickness
        )
        cv2.rectangle(
            frame,
            (x, y),
            (x + text_w, y - text_h),
            self.font_background,
            cv2.FILLED,
        )
        cv2.putText(
            frame,
            text,
            (x, y),
            self.font,
            self.font_size,
            font_color,
            self.font_thickness,
        )

        return frame

    def __del__(self):
        self.video.release()

    def predict_yolo(self):
        frame_counter = 0
        while self.video.isOpened():
            _, frame = self.video.read()
            # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            if frame_counter % self.hop == 0:
                image = self.model(frame, size=IMG_SIZE)
                names = image.names
                # image = image.imgs[0]
                coord = image.xyxy[0].detach().cpu().numpy()

                for (x1, y1, x2, y2, conf, name) in coord:
                    # print((x1, y1, x2, y2, conf, name))
                    process([float(conf)], [int(name)])
                    letter = names[int(name)]
                    cv2.rectangle(
                        frame,
                        (int(x1), int(y1)),
                        (int(x2), int(y2)),
                        BLUE,
                        2,
                    )
                    self.buffer = collections.deque([" "] * 20)
                    for i in range(len(output_string)):
                        self.buffer.popleft()
                        self.buffer.append(names[int(output_string[i])])
                    frame = self.draw_text(
                        frame, letter, int(x1), int(y1), conf
                    )
            # print(self.buffer)
            frame = self.draw_text(
                frame, name=self.get_buffer(), x=5, y=30, font_color=BLUE
            )

            frame = cv2.imencode(".jpg", frame)[1].tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
            )

    def get_buffer(self):
        return "".join(list(self.buffer))
