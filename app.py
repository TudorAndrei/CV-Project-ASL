from flask import Flask, render_template
from flask.wrappers import Response
from camera import VideoCamera
import threading
import time
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)

video_stream = VideoCamera()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/yolo")
def yolo_mainpage():
    return render_template("yolo.html")


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()


def update_load():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(
                turbo.replace(
                    render_template(
                        "yolo.html", text=video_stream.get_prediction()
                    ),
                    "load",
                )
            )


@app.route("/yoloer")
def yolo_page():
    return Response(
        video_stream.predict_yolo(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=5000, threaded=True)
