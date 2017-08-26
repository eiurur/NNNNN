#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import tensorflow as tf
import tensorflow.python.platform
from Trainer import Trainer


if __name__ == '__main__':
    with tf.Session() as sess:
        trainer = Trainer(sess)
        trainer.train()
        trainer.test()
        trainer.save()
