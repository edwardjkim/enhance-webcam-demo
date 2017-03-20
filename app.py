async_mode = "eventlet"
from eventlet import wsgi, websocket
import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, session, request, Response
from flask_socketio import SocketIO, emit, disconnect
import base64

from video import Video


app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html', async_mode=socketio.async_mode)


def gen(video):
    """Video streaming generator function."""
    while True:
        frame = video.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/original_video_feed')
def original_video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Video('original_images', 25)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/upsampled_video_feed')
def upsampled_video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Video('upsampled_images', 25)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on('frame', namespace='/')
def user_video(frame):
    feed = frame
    print(str(feed))


if __name__ == '__main__':

    eventlet.wsgi.server(
        eventlet.wrap_ssl(
            eventlet.listen(('', 8443)),
            certfile='server.crt',
            keyfile='server.key',
            server_side=True),
        app)
