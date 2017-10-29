#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tensorflow as tf
import tensorflow.python.platform
from os import path


import configparser
config = configparser.ConfigParser()
config.read(path.abspath(path.join('configs', 'setting.ini')))
CONFIG_SECTION = 'development'

CLASSES_NUM = int(config.get(
    CONFIG_SECTION, "CLASSES_NUM"))
IMAGE_SIZE_PX = int(config.get(
    CONFIG_SECTION, "IMAGE_SIZE_PX"))
IMAGE_PIXELS = IMAGE_SIZE_PX * IMAGE_SIZE_PX * 3


def inference(images_placeholder, keep_prob):
    ###############################################################
    #   ディープラーニングのモデルを作成する関数
    # 引数:
    #  images_placeholder: inputs()で作成した画像のplaceholder
    #  keep_prob: dropout率のplace_holder
    # 返り値:
    #  cross_entropy: モデルの計算結果
    ###############################################################
    # 重みを標準偏差0.1の正規分布で初期化
    def weight_variable(shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    # バイアスを標準偏差0.1の正規分布で初期化
    def bias_variable(shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    # 畳み込み層の作成
    def conv2d(x, W):
        # return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    # プーリング層の作成
    def max_pool(x, w, h):
        return tf.nn.max_pool(x, ksize=[1, w, h, 1],
                              strides=[1, w, h, 1], padding='SAME')
    # 入力を28x28x3に変形
    x_images = tf.reshape(images_placeholder,
                          [-1, IMAGE_SIZE_PX, IMAGE_SIZE_PX, 3])

    # 畳み込み層1の作成
    with tf.name_scope('conv1') as scope:
        W_conv1 = weight_variable([3, 3, 3, 16])
        b_conv1 = bias_variable([16])
        h_conv1 = tf.nn.relu(conv2d(x_images, W_conv1) + b_conv1)

    # プーリング層1の作成
    with tf.name_scope('pool1') as scope:
        h_pool1 = max_pool(h_conv1, 2, 2)

    # 畳み込み層2の作成
    with tf.name_scope('conv2') as scope:
        W_conv2 = weight_variable([3, 3, 16, 32])
        b_conv2 = bias_variable([32])
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

    # プーリング層2の作成
    with tf.name_scope('pool2') as scope:
        h_pool2 = max_pool(h_conv2, 2, 2)

    # 畳み込み層3の作成
    with tf.name_scope('conv3') as scope:
        W_conv3 = weight_variable([3, 3, 32, 48])
        b_conv3 = bias_variable([48])
        h_conv3 = tf.nn.relu(conv2d(h_pool2, W_conv3) + b_conv3)

    # プーリング層3の作成
    with tf.name_scope('pool3') as scope:
        h_pool3 = max_pool(h_conv3, 2, 2)

    # 畳み込み層4の作成
    with tf.name_scope('conv4') as scope:
        W_conv4 = weight_variable([3, 3, 48, 64])
        b_conv4 = bias_variable([64])
        h_conv4 = tf.nn.relu(conv2d(h_pool3, W_conv4) + b_conv4)

    # プーリング層4の作成
    with tf.name_scope('pool4') as scope:
        h_pool4 = max_pool(h_conv4, 2, 2)

    # 全結合層1の作成
    with tf.name_scope('fc1') as scope:
        W_fc1 = weight_variable(
            [int(IMAGE_SIZE_PX / 16) * int(IMAGE_SIZE_PX / 16) * 64, 4096])
        b_fc1 = bias_variable([4096])
        h_pool4_flat = tf.reshape(
            h_pool4, [-1, int(IMAGE_SIZE_PX / 16) * int(IMAGE_SIZE_PX / 16) * 64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool4_flat, W_fc1) + b_fc1)
        # dropoutの設定
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # 全結合層2の作成
    with tf.name_scope('fc2') as scope:
        W_fc2 = weight_variable([4096, CLASSES_NUM])
        b_fc2 = bias_variable([CLASSES_NUM])

    # ソフトマックス関数による正規化
    with tf.name_scope('softmax') as scope:
        y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    return y_conv


def loss(logits, labels):
    ###############################################################
    #   lossを計算する関数
    # 損失関数とは、ニューラルネットワークが教師データに対してどれだけ適合していないかを算出する関数であり
    # ニューラルネットワークの性能の悪さを示す指標となります。機械学習の目標はこの値を0に近づけること
    # 引数:
    #  logits: ロジットのtensor, float - [batch_size, CLASSES_NUM]
    #  labels: ラベルのtensor, int32 - [batch_size, CLASSES_NUM]
    # 返り値:
    #  cross_entropy: モデルの計算結果
    ###############################################################
    cross_entropy = - \
        tf.reduce_sum(labels * tf.log(tf.clip_by_value(logits, 1e-10, 1.0)))
    tf.summary.scalar("cross_entropy", cross_entropy)
    return cross_entropy


def training(loss, learning_rate):
    ###############################################################
    #   訓練のOpを定義する関数
    # 引数:
    #  loss: 損失のtensor, loss()の結果
    #  learning_rate: 学習係数
    # 返り値:
    #  train_step: 訓練のOp
    ###############################################################
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss)
    return train_step


def accuracy(logits, labels):
    ###############################################################
    #   正解率(accuracy)を計算する関数
    # 引数:
    #  logits: inference()の結果
    #  labels: ラベルのtensor, int32 - [batch_size, CLASSES_NUM]
    # 返り値:
    #  accuracy: 正解率(float)
    ###############################################################
    correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(labels, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    tf.summary.scalar("accuracy", accuracy)
    return accuracy
