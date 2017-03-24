import os
import sys
import threading
import numpy as np
import tensorflow as tf
from scipy.misc import imread, imsave


sys.path.insert(0, './enhance')
import sres


def start_tf_session(checkpoint_dir, input_shape=[1, 2, 90, 120, 3]):

    input_images = tf.placeholder(tf.float32, shape=input_shape)
    output_image = sres.generator(input_images)

    tf.get_variable_scope().reuse_variables()
    saver = tf.train.Saver() 

    with tf.Session() as sess:
        ckpt = tf.train.get_checkpoint_state(checkpoint_dir)

    saver.restore(sess, ckpt.model_checkpoint_path)

    return sess, output_image, input_images


def predict_and_save(sess, graph, variable, data, ofilename, num_threads=1):

    input_images = tf.placeholder(tf.float32, shape=[1, 2, 90, 120, 3])
    output_image = sres.generator(input_images)
   
    tf.get_variable_scope().reuse_variables()
    saver = tf.train.Saver() 
   
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:
   
        saver.restore(sess, 'model/model.ckpt-99999')
   
        #coord = tf.train.Coordinator()
        #
        #threads = [
        #    threading.Thread(
        #        target=_predict_and_save,
        #        args=(coord, sess, output_image, input_images, data, ofilename))
        #    for i in xrange(num_threads)]
    
        #for t in threads:
        #    t.start()
        #coord.join(threads)
    
        #coord.request_stop()
        #coord.join(threads)
        generated_images = sess.run(output_image, feed_dict={input_images: data})
        imsave(ofilename, generated_images[0, 1])

    #generated_images = sess.run(graph, feed_dict={variable: data})
    #imsave(ofilename, generated_images[0, 1])


def _predict_and_save(coord, sess, graph, variable, data, ofilename):

    while not coord.should_stop():
        generated_images = sess.run(graph, feed_dict={variable: data})
        imsave(ofilename, generated_images[0, 1])


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


