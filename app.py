from flask import Flask, render_template, session, request, Response, redirect, url_for
import os
import sys
import base64
import urllib
import re

from PIL import Image
import cStringIO
import numpy as np
from scipy.misc import imread, imsave
import tensorflow as tf

sys.path.insert(0, './enhance')
import sres


input_images = tf.placeholder(tf.float32, shape=[1, 2, 90, 120, 3])
output_images = sres.generator(input_images)

tf.get_variable_scope().reuse_variables()
saver = tf.train.Saver() 

sess = tf.Session()

saver.restore(sess, 'model/model.ckpt-99999')


app = Flask(__name__)


def predict_and_save(data, filename):

    generated_images = sess.run(output_images, feed_dict={input_images: data})
    imsave(filename, generated_images[0, 1])


def process_frames(previous_frame, current_frame, shape=(90, 120, 3)):

    if os.path.exists(previous_frame):
        previous_image = imread(previous_frame)
    else:
        previous_image = np.ones(shape)

    if os.path.exists(current_frame):
        current_image = imread(current_frame)
    else:
        current_image = np.ones(shape)

    images = np.stack([[previous_image, current_image]])
    images = images / 127.5 - 1.0

    return images


@app.route('/', methods=['GET', 'POST'])
def index():
    """Video streaming home page."""
    if request.method == 'GET':

        return render_template('index.html')

    if request.method == 'POST':
        
        image_b64 = request.form['frame_data']
        image_data = re.sub('^data:image/.+;base64,', '', image_b64)
        image_data = image_data.decode('base64')

        if os.path.exists('static/current_frame.jpg'):
            os.rename('static/current_frame.jpg', 'static/previous_frame.jpg')

        with open('static/current_frame.jpg', 'w') as f:
            f.write(image_data)

        input_images = process_frames('static/previous_frame.jpg', 'static/current_frame.jpg')
        predict_and_save(input_images, 'static/upsampled_frame.jpg')

        return ''


@app.route('/view')
def view():
    """Video streaming home page."""
    return render_template('view.html')


if __name__ == '__main__':

    app.run(debug=True)
