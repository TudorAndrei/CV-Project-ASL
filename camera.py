import cv2
import torch


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
        sample_rate = 5
        fps = round(self.video.get(cv2.CAP_PROP_FPS))
        self.hop = round(fps / sample_rate)
        # if use_model:
        #     self.model = torch.load(r"models/best.pt")
        self.model = torch.hub.load("ultralytics/yolov5", "yolov5s")
        self.model.conf = 0.5

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
        BLACK = (255, 255, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1.1
        font_color = BLACK
        font_thickness = 2
        while self.video.isOpened():
            _, frame = self.video.read()

            # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            image = self.model(frame, size=640)
            names = image.names
            # image = image.imgs[0]
            coord = image.xyxy[0].detach().cpu().numpy()

            for (x1, y1, x2, y2, conf, name) in coord:
                #     print((x1, y1, x2, y2, conf, name))
                cv2.rectangle(
                    frame,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (255, 245, 67),
                    2,
                )
                cv2.putText(
                    frame,
                    f"{names[int(name)]} {100*conf:.0f}%",
                    (int(x1), int(y1)),
                    font,
                    font_size,
                    font_color,
                    font_thickness,
                    cv2.LINE_AA,
                )

            frame = cv2.imencode(".jpg", frame)[1].tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
            )
