#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import codecs
from os import path
import pickle
import cv2
import csv
import numpy as np
import random
import time
from datetime import datetime
import tensorflow as tf
import tensorflow.python.platform
import configparser

lib_dir = path.abspath(path.join("lib"))
sys.path.append(lib_dir)
from CsvFile import CsvFile
from dlfunc import *

import configparser
config = configparser.ConfigParser()
config.read(path.abspath(path.join('configs', 'setting.ini')))
CONFIG_SECTION = 'development'

CLASSES_NUM = int(config.get(
    CONFIG_SECTION, "CLASSES_NUM"))
IMAGE_SIZE_PX = int(config.get(
    CONFIG_SECTION, "IMAGE_SIZE_PX"))
IMAGE_PIXELS = IMAGE_SIZE_PX * IMAGE_SIZE_PX * 3

# Number of steps to run trainer
MAX_STEPS = int(config.get(
    CONFIG_SECTION, "MAX_STEPS"))

# Must divide evenly into the dataset sizes.
BATCH_SIZE = int(config.get(
    CONFIG_SECTION, "BATCH_SIZE"))

# Initial learning rate
LEARNING_RATE = float(config.get(
    CONFIG_SECTION, "LEARNING_RATE"))

# File name of model data
SAVE_MODEL = path.abspath(path.join('models', 'model.ckpt'))

# File name of train data
TRAIN_DATA = path.abspath(path.join('3_train', 'training', 'train.txt'))

# File name of test data
TEST_DATA = path.abspath(path.join('3_train', 'training', 'test.txt'))


# http://stackoverflow.com/questions/17649875/why-does-random-shuffle-return-non
def shuffle(list, num=BATCH_SIZE):
    return random.sample(list, len(list))


def separate_list(list, num):
    return list[:num], list[-num:]


def get_image_and_label(csv_lines):
    images = []
    labels = []
    for train in csv_lines:
        try:
            image = cv2.imread(train[0])
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = image.flatten().astype(np.float32) / 255.0
            images.append(image)
            label_box = np.zeros(int(config.get(
                CONFIG_SECTION, "CLASSES_NUM")))
            label_box[int(train[1])] = 1
            labels.append(label_box)
        except OSError as err:
            print("OSError: {0}".format(err))
        except Exception as e:
            print("Exception args:", e.args)
            print(train[0])
        except:
            print("Waht happened!!")
            # print(sys.exc_info())
            import traceback

    return np.asarray(images, dtype=np.float32), np.asarray(labels, dtype=np.float32)


class Trainer:
    def __init__(self, sess):
        self.sess = sess
        self.images_placeholder = tf.placeholder(
            tf.float32, shape=(None, IMAGE_PIXELS))
        self.labels_placeholder = tf.placeholder(
            tf.float32, shape=(None, CLASSES_NUM))
        self.keep_prob = tf.placeholder(tf.float32)

        self.logits = inference(self.images_placeholder, self.keep_prob)
        self.loss_value = loss(self.logits, self.labels_placeholder)
        self.train_op = training(self.loss_value, LEARNING_RATE)
        self.acc = accuracy(self.logits, self.labels_placeholder)

        self.sess.run(tf.global_variables_initializer())

    ###
    # Train Phaseb
    ###
    def train(self):
        for step in range(MAX_STEPS):

            # 計測
            start_time = time.time()

            # 訓練の実行
            train_csv = CsvFile(TRAIN_DATA)
            trains = train_csv.read()
            random.shuffle(trains)
            train_len = len(trains)

            train_batch_add = 0 if train_len % BATCH_SIZE is 0 else 1
            train_batch = (train_len / BATCH_SIZE) + train_batch_add

            for i in range(int(train_len / BATCH_SIZE)):
                batch = BATCH_SIZE * i
                batch_plus = BATCH_SIZE * (i + 1)
                if batch_plus > train_len:
                    batch_plus = train_len
                train_image, train_label = get_image_and_label(
                    trains[batch:batch_plus])

                # feed_dictでplaceholderに入れるデータを指定する
                self.sess.run(self.train_op, feed_dict={
                    self.images_placeholder: train_image,
                    self.labels_placeholder: train_label,
                    self.keep_prob: 0.8})

            duration = time.time() - start_time

            shuffled_trains, _ = separate_list(
                shuffle(trains), BATCH_SIZE * 50)
            all_train_image, all_train_label = get_image_and_label(
                shuffled_trains)

            # 1 step終わるたびにTensorBoardに表示する値を追加する
            # summary_str = self.sess.run(self.summary_op, feed_dict={
            #     self.images_placeholder: all_train_image,
            #     self.labels_placeholder: all_train_label,
            #     self.keep_prob: 1.0})
            # summary_writer.add_summary(summary_str, step)

            # 10 step終わるたびに精度を計算する
            if step % 10 == 0:

                num_examples_per_step = BATCH_SIZE
                examples_per_sec = num_examples_per_step / duration
                sec_per_batch = float(duration)

                train_accuracy = 0.0
                train_accuracy += self.sess.run(self.acc, feed_dict={
                    self.images_placeholder: all_train_image,
                    self.labels_placeholder: all_train_label,
                    self.keep_prob: 1.0})

                format_str = ('%s: step %d, training accuracy %g (%.1f examples/sec; %.3f '
                              'sec/batch)')
                print(format_str % (datetime.now(), step,
                                    train_accuracy, examples_per_sec, sec_per_batch))

                # 前回と精度が同じなら学習終了
                # if train_accuracy == previous_train_accuracy:
                #     break

    ###
    # Test Phase
    ###
    def test(self):
        test_csv = CsvFile(TEST_DATA)
        tests = test_csv.read()

        # tests = loadFromCsv(FLAGS.test)[0:]
        test_len = len(tests)
        test_accuracy = 0.0
        test_image, test_label = get_image_and_label(tests)
        test_accuracy += self.sess.run(self.acc, feed_dict={
            self.images_placeholder: test_image,
            self.labels_placeholder: test_label,
            self.keep_prob: 1.0})
        print("test accuracy %g" % (test_accuracy))

    def save(self):
        saver = tf.train.Saver()
        saver.save(self.sess, SAVE_MODEL)
