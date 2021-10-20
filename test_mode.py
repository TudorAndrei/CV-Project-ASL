import cv2
import torch


vid = cv2.VideoCapture(0)
# model = torch.hub.load(
#     "yolov5", "custom", path="models/best.pt", source="local"
# )
model = torch.hub.load("ultralytics/yolov5", "yolov5s")

BLACK = (255, 255, 255)
font = cv2.FONT_HERSHEY_SIMPLEX
font_size = 1.1
font_color = BLACK
font_thickness = 2

while True:

    #     # Capture the video frame
    #     # by frame
    ret, frame = vid.read()
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    image = model(frame, size=320)
    names = image.names
    # image = image.imgs[0]
    coord = image.xyxy[0].detach().cpu().numpy()

    #     # Display the resulting frame

    for (x1, y1, x2, y2, conf, name) in coord:
        #     print((x1, y1, x2, y2, conf, name))
        cv2.rectangle(
            frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 245, 67), 2
        )
        cv2.putText(
            frame,
            f"{names[int(name)]} {100*conf:.0f} $",
            (int(x1), int(y1)),
            font,
            font_size,
            font_color,
            font_thickness,
            cv2.LINE_AA,
        )
    cv2.imshow("frame", frame)

    #     # the 'q' button is set as the
    #     # quitting button you may use any
    #     # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# # After the loop release the cap object
vid.release()
# # Destroy all the windows
cv2.destroyAllWindows()
