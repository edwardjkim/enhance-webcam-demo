async_mode = "eventlet"
from eventlet import wsgi, websocket
import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, session, request, Response, redirect, url_for
from flask_socketio import SocketIO, emit, disconnect

import os
import base64
import re
from PIL import Image
import cStringIO
import numpy as np
from scipy.misc import imsave

from video import Video


app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Video streaming home page."""
    if request.method == 'GET':

        return render_template('index.html', async_mode=socketio.async_mode)

    if request.method == 'POST':

        image_b64 = request.form['frame_data']
        image_data = re.sub('^data:image/.+;base64,', '', image_b64)
        image_data = image_data.decode('base64')

        if os.path.exists('static/current_frame.png'):
            os.rename('static/current_frame.png', 'static/previous_frame.png')

        with open('static/current_frame.png', 'w') as f:
            f.write(image_data)

        return Response('OK')


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
