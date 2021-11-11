import cv2
import torch
from collections import deque

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (255, 245, 67)
IMG_SIZE = 320


class VideoCamera(object):
    def __init__(self):
        try:
            self.video = cv2.VideoCapture(-1)
        except:
            print("Camera not initialized")
        self.hand_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "aGest.xml"
        )
        self.eye_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_eye.xml"
        )
        sample_rate = 10
        fps = round(self.video.get(cv2.CAP_PROP_FPS))
        self.hop = round(fps / sample_rate)
        # if use_model:
        #     self.model = torch.load(r"models/best.pt")

        self.model = torch.hub.load(
            "yolo",
            "custom",
            path="best.pt",
            source="local",
        )
        # self.model = torch.hub.load("ultralytics/yolov5", "yolov5l")
        self.model.conf = 0.5
        self.seq = []
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_size = 1.1
        self.font_color = WHITE
        self.font_background = BLACK
        self.font_thickness = 2
        self.prection = ""
        self.buffer = deque([" "] * 20)

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

    def detect_eyes(self):
        frame_counter = 0
        while self.video.isOpened():
            _, frame = self.video.read()
            # print(frame.shape)

            if frame_counter % self.hop == 0:

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                try:
                    eyes = self.eye_detector.detectMultiScale(gray)
                    for (x, y, w, h) in eyes:
                        cv2.rectangle(
                            frame, (x, y), (x + w, y + h), (255, 245, 67), 10
                        )
                except:
                    print("No detection")

            frame = cv2.imencode(".jpg", frame)[1].tobytes()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
            )

    def detect_hands(self):
        while self.video.isOpened():
            _, frame = self.video.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            try:

                hands = self.hand_detector.detectMultiScale(gray)
                for (x, y, w, h) in hands:
                    cv2.rectangle(
                        frame, (x, y), (x + w, y + h), (255, 245, 67), 10
                    )
            except:
                print("No detection")

            frame = cv2.imencode(".jpg", frame)[1].tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
            )

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
                    #     print((x1, y1, x2, y2, conf, name))
                    letter = names[int(name)]
                    cv2.rectangle(
                        frame,
                        (int(x1), int(y1)),
                        (int(x2), int(y2)),
                        BLUE,
                        2,
                    )

                    frame = self.draw_text(
                        frame, letter, int(x1), int(y1), conf
                    )
                    if letter != self.buffer[-1]:
                        self.buffer.popleft()
                        self.buffer.append(names[int(name)])

            text = "".join(list(self.buffer))
            frame = self.draw_text(
                frame, name=text, x=5, y=30, font_color=BLUE
            )

            # if coord != []:
            #     print(f"conf{coord[:,4]}, letter {coord[:,5]}")
            # else:
            #     print("No detect")

            frame = cv2.imencode(".jpg", frame)[1].tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
            )
