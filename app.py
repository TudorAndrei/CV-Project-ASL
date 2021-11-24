from flask import Flask, request, jsonify, render_template
from flask.wrappers import Response
from camera import VideoCamera
import random, os

app = Flask(__name__)

picFolder = os.path.join("static", "images")
app.config["UPLOAD_FOLDER"] = picFolder
image1 = os.path.join(app.config["UPLOAD_FOLDER"], "ASLalphabet1.png")
image2 = os.path.join(app.config["UPLOAD_FOLDER"], "ASLalphabet2.png")
video_stream = VideoCamera()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/yolo")
def yolo_mainpage():
    return render_template("yolo.html", asl1 = image1, asl2 = image2)


@app.route("/yoloer")
def yolo_page():
    return Response(
        video_stream.predict_yolo(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route('/_stuff', methods=['GET'])
def stuff():
    if video_stream.get_buffer()[-1] != " ":
        result = video_stream.get_buffer()
    else:
        result = "Result"
    return jsonify(result=result)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=5000, threaded=True)
