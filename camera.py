import cv2
import numpy as np


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # self.hand_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "aGest.xml")

    def __del__(self):
        self.video.release()

    def detect_eyes(self):
        hand_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_eye.xml"
        )
        while self.video.isOpened():
            _, frame = self.video.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            try:

                hands = hand_detector.detectMultiScale(gray)
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

    def detect_hands(self):
        while self.video.isOpened():
            _, frame = self.video.read()
            print("Image shape")
            print(frame.shape)
            frame = cv2.bilateralFilter(frame, 5, 50, 100)  # Smoothing
            frame = cv2.flip(frame, 1)  # Horizontal Flip

            bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)
            fgmask = bgModel.apply(frame)

            kernel = np.ones((3, 3), np.uint8)
            fgmask = cv2.erode(fgmask, kernel, iterations=1)
            img = cv2.bitwise_and(frame, frame, mask=fgmask)

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower = np.array([0, 48, 80], dtype="uint8")
            upper = np.array([20, 255, 255], dtype="uint8")
            skinMask = cv2.inRange(hsv, lower, upper)

            frame = cv2.imencode(".jpg", skinMask)[1].tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
            )
