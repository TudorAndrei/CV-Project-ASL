from flask import Flask, render_template
from flask.wrappers import Response
from camera import VideoCamera

app = Flask(__name__)

video_stream = VideoCamera()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/yolo")
def yolo_mainpage():
    return render_template("yolo.html")


@app.route("/yoloer")
def yolo_page():
    return Response(
        video_stream.predict_yolo(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=5000, threaded=True)
