#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path
import numpy as np
import tensorflow as tf
import urllib
import io
from PIL import Image
from types import *
import configparser
from dlfunc import *

config = configparser.ConfigParser()
config.read(path.abspath(path.join('configs', 'setting.ini')))
CONFIG_SECTION = 'development'

CLASSES_NUM = int(config.get(
    CONFIG_SECTION, "CLASSES_NUM"))
IMAGE_SIZE_PX = int(config.get(
    CONFIG_SECTION, "IMAGE_SIZE_PX"))
IMAGE_PIXELS = IMAGE_SIZE_PX * IMAGE_SIZE_PX * 3
READ_MODELS = path.abspath(path.join('models', 'model.ckpt'))

###
# DeepLearning関連
###
images_placeholder = tf.placeholder("float", shape=(None, IMAGE_PIXELS))
labels_placeholder = tf.placeholder("float", shape=(None, CLASSES_NUM))
keep_prob = tf.placeholder("float")
logits = inference(images_placeholder, keep_prob)

sess = tf.InteractiveSession()
saver = tf.train.Saver()
sess.run(tf.global_variables_initializer())
saver.restore(sess, READ_MODELS)


def get_IMAGE_SIZE_PX(file):
    img = Image.open(io.BytesIO(file))
    return (img.width, img.height)


def get_tensor_from_url(url):
    with tf.Session() as sess:
        file = urllib.request.urlopen(url).read()
        width, height = get_IMAGE_SIZE_PX(file)
        long_size_px = height if height > width else width
        image = tf.image.decode_image(file, channels=3)
        image = tf.image.resize_image_with_crop_or_pad(
            image, long_size_px, long_size_px)
        image = tf.image.resize_images(image, [IMAGE_SIZE_PX, IMAGE_SIZE_PX])
        image_val = sess.run(image).flatten().astype(np.float32) / 255.0
        return image_val


def classify(urls):

    test_image = []
    for i in range(len(urls)):
        test_image.append(get_tensor_from_url(urls[i]))
    test_image = np.asarray(test_image)

    for i in range(len(test_image)):
        pr = logits.eval(feed_dict={
            images_placeholder: [test_image[i]],
            keep_prob: 1.0})[0]
        pred = np.argmax(pr)
        prmax = np.max(pr)
        print(pr)
        print(prmax)
        print(pred)

    if prmax < 0.6:
        pred = CLASSES_NUM

    return [pr, pred]
