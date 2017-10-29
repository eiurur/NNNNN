#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path
import tensorflow as tf
import tensorflow.python.platform
from Trainer import Trainer

lib_dir = path.abspath(path.join("lib"))
sys.path.append(lib_dir)
from Notifier import Notifier


if __name__ == '__main__':
    # tf_config = tf.ConfigProto(
    #     gpu_options=tf.GPUOptions(
    #         allow_growth=True  # True->必要になったら確保, False->全部
    #     )
    # )
    # with tf.Session(config=tf_config) as sess:
    with tf.Session() as sess:
        trainer = Trainer(sess)
        trainer.train()
        trainer.test()
        trainer.save()
        notifier = Notifier()
        notifier.notify("Finish train", trainer.output())
