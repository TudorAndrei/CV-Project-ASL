from flask import Flask, render_template, Response
from camera import VideoCamera

app = Flask(__name__)

video_stream = VideoCamera()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/eye_detect")
def eye_detect_page():
    return Response(
        video_stream.detect_eyes(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/hand_detect")
def hand_detect():
    return Response(
        video_stream.detect_hands(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port="5000")
