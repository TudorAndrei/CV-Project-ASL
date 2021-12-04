import collections
import camera_utils

import cv2
import torch

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (255, 245, 67)
IMG_SIZE = 640

CAMERA_INDEX = 0
CONF_TRESHOLD = 0.3
FONT = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self):
        try:
            self.video = cv2.VideoCapture(CAMERA_INDEX)
        except:
            print("Camera not initialized")
        sample_rate = 30
        fps = round(self.video.get(cv2.CAP_PROP_FPS))
        self.hop = round(fps / sample_rate)

        self.model = torch.hub.load(
            "yolo",
            "custom",
            # path="models/best.pt",
            path="models/train_medium/best.pt",
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
                    camera_utils.process([float(conf)], [int(name)])
                    letter = names[int(name)]
                    cv2.rectangle(
                        frame,
                        (int(x1), int(y1)),
                        (int(x2), int(y2)),
                        BLUE,
                        2,
                    )
                    self.buffer = collections.deque([" "] * 20)
                    for i in range(len(camera_utils.output_string)):
                        self.buffer.popleft()
                        self.buffer.append(names[int(camera_utils.output_string[i])])
                    frame = self.draw_text(
                        frame, letter, int(x1), int(y1), conf
                    )
            # print(self.buffer)
            # frame = self.draw_text(
            #     frame, name=self.get_buffer(), x=5, y=30, font_color=BLUE
            # )

            frame = cv2.imencode(".jpg", frame)[1].tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
            )

    def get_buffer(self):
        return "".join(list(self.buffer))
