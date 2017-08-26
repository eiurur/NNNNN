#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import tensorflow as tf
import tensorflow.python.platform


class Image:
    def __init__(self, file_path, length):
        self.file_path = file_path
        self.length = length

    def decode(self):
        im_encoded = tf.read_file(self.file_path)
        return tf.image.decode_image(im_encoded, channels=3)

    def info(self):
        cv_img = cv2.imread(self.file_path)
        return cv_img.shape[:3]

    # 画像変換(clop and padding -> resize)
    def transform(self, sess):
        height, width, channels = self.info()
        long_side_px = height if height > width else width
        image = self.decode()
        image = tf.image.resize_image_with_crop_or_pad(
            image, long_side_px, long_side_px)
        image = tf.image.resize_images(image, [self.length, self.length])
        image = sess.run(image)
        return image

    def write(self, sess, dest):
        rgb_image = cv2.cvtColor(self.transform(sess), cv2.COLOR_BGR2RGB)
        cv2.imwrite(dest, rgb_image)
