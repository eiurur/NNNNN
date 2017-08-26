#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path
from Siwake import Siwake

import configparser
config = configparser.ConfigParser()
config.read(path.abspath(path.join('configs', 'setting.ini')))
CONFIG_SECTION = 'development'

CLASSES_NUM = int(config.get(
    CONFIG_SECTION, "CLASSES_NUM"))

if __name__ == '__main__':
    print(sys.argv)
    filename = sys.argv[1]
    siwake = Siwake(filename, separator=",")

    if '--test' in sys.argv:
        image_dirname = 'test_images'
    else:
        image_dirname = 'images'

    category_set_list = [{
        "directory": "{}/{}/{}".format(path.abspath('1_generate_csv'), image_dirname, i),
        "label": str(i)
    } for i in range(CLASSES_NUM)]

    print(category_set_list)

    siwake.load(category_set_list)

    siwake.write()
