from flask import Flask, request, jsonify, render_template
from flask.wrappers import Response
from camera import VideoCamera
import random, os

data = ['mother', 'father', 'brother', 'sister', 'hi', 'apple', 'maple', 'pear', 'you', 'one']

app = Flask(__name__)

picFolder = os.path.join("static", "images")
app.config["UPLOAD_FOLDER"] = picFolder
image1 = os.path.join(app.config["UPLOAD_FOLDER"], "ASLalphabet1.png")
image2 = os.path.join(app.config["UPLOAD_FOLDER"], "ASLalphabet2.png")
video_stream = VideoCamera()

word = "Here will be your word"
data2 = []

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/yolo")
def yolo_mainpage():
    return render_template("yolo.html", asl1 = image1, asl2 = image2, the_word=word)


@app.route("/yoloer")
def yolo_page():
    return Response(
        video_stream.predict_yolo(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )

@app.route("/play")
def get_word():
    global data, data2, word
    if not data:
        data.extend(data2)
        data.remove(word)
        data2.clear()
        data2.append(word)
    word = random.choice(data)
    print(word)
    print(data)
    print(data2)
    data.remove(word)
    data2.append(word)
    return render_template("yolo.html", asl1=image1, asl2=image2, the_word=word)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=5000, threaded=True)
