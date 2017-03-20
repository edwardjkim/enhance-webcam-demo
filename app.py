async_mode = "eventlet"
from eventlet import wsgi, websocket
import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, session, request, Response, redirect, url_for
from flask_socketio import SocketIO, emit, disconnect
import base64

from video import Video


app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Video streaming home page."""
    if request.method == 'GET':
        return render_template('index.html', async_mode=socketio.async_mode)
    if request.method == 'POST':
        data = request.form['frame_data']
        with open("test.png", "wb") as f:
            f.write(data)
        return redirect(url_for('snapshot'))    


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
