import cv2

camera = cv2.VideoCapture(0)

eye_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
face_casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

while True:

    ret, frame = camera.read()
    gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # faces = face_casc.detectMultiScale(gray, 1.2, 5, minSize=(30,30), flags=cv2.CASCADE_SCALE_IMAGE)


    eyes = eye_detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    for (x, y, w, h) in eyes:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 245, 67), 10)

    cv2.imshow("Video Frame", frame)

    if cv2.waitKey(1) == ord('q'):

        break

camera.release()
cv2.destroyAllWindows()
