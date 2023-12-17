from flask import Flask, Response
import cv2
from environs import Env

app = Flask(__name__)

env = Env()
env.read_env()
video_device = int(env("VIDEO_DEVICE", default='0'))
video_link = env("VIDEO_LINK", default="video_feed")

camera = cv2.VideoCapture(video_device)


def generate_frames():
    while True:
        success, frame = camera.read()
        frame = cv2.resize(frame, (1024, 680))
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route(f'/{video_link}')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=False)
