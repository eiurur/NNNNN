#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path, makedirs

import configparser
config = configparser.ConfigParser()
config.read(path.abspath(path.join('configs', 'setting.ini')))
CONFIG_SECTION = 'development'

CLASSES_NUM = int(config.get(
    CONFIG_SECTION, "CLASSES_NUM"))


class F:
    def __init__(self, folder_path, folder_num):
        self.folder_path = folder_path
        self.folder_num = folder_num

    def create(self):
        for i in range(self.folder_num):
            directory = "{}/{}".format(self.folder_path, i)
            if not path.exists(directory):
                makedirs(directory)
                print("created: {}".format(directory))


[f.create() for f in [
    F(path.abspath(path.join('1_generate_csv', 'images')), CLASSES_NUM),
    F(path.abspath(path.join('1_generate_csv', 'test_images')), CLASSES_NUM),
    F(path.abspath(path.join('2_preprocess', 'images')), CLASSES_NUM),
    F(path.abspath(path.join('2_preprocess', 'test_images')), CLASSES_NUM),
    F(path.abspath(path.join('4_collect', 'images')), CLASSES_NUM + 1)
]]
