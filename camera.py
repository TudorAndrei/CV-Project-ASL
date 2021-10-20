import cv2


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

    def __del__(self):
        self.video.release()

    def detect_eyes(self):
        while self.video.isOpened():
            _, frame = self.video.read()

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
        _, frame = self.video.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        hands = self.hand_detector.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=5
        )
        for (x, y, w, h) in hands:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 245, 67), 10)

        _, jpeg = cv2.imencode(".jpg", frame)

        return jpeg.tobytes()
