async_mode = "eventlet"
from eventlet import wsgi, websocket
import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, session, request, Response, redirect, url_for
from flask_socketio import SocketIO, emit, disconnect

import os
import sys
import base64
import urllib
import re
from PIL import Image
import cStringIO
import numpy as np
from scipy.misc import imsave
import tensorflow as tf
from OpenSSL import SSL

import tf_ops

app = Flask(__name__)
socketio = SocketIO(app)

#sess, output_graph, input_var = tf_ops.start_tf_session('model/model.ckpt-999')
sess = None
output_graph = None
input_var = None

@app.route('/client', methods=['GET', 'POST'])
def index():
    """Video streaming home page."""
    if request.method == 'GET':

        return render_template('index.html', async_mode=socketio.async_mode)

    if request.method == 'POST':
        
        image_b64 = request.form['frame_data']
        image_data = re.sub('^data:image/.+;base64,', '', image_b64)
        image_data = image_data.decode('base64')

        if os.path.exists('static/current_frame.jpg'):
            os.rename('static/current_frame.jpg', 'static/previous_frame.jpg')

        with open('static/current_frame.jpg', 'w') as f:
            f.write(image_data)

        input_images = tf_ops.process_frames('static/previous_frame.jpg', 'static/current_frame.jpg')
        tf_ops.predict_and_save(sess, output_graph, input_var, input_images, 'static/upsampled_frame.jpg')

        return ''


if __name__ == '__main__':

    eventlet.wsgi.server(
        eventlet.wrap_ssl(
            eventlet.listen(('', 8443)),
            certfile='server.crt',
            keyfile='server.key',
            server_side=True),
        app)
