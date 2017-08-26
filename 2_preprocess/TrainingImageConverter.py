#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path
import tensorflow as tf
import tensorflow.python.platform
import configparser

lib_dir = path.abspath(path.join("lib"))
sys.path.append(lib_dir)
from Image import Image
from CsvFile import CsvFile

config = configparser.ConfigParser()
config.read(path.abspath(path.join('configs', 'setting.ini')))
CONFIG_SECTION = 'development'


class TrainingImageConverter:
    def __init__(self, dataset_path, output_file_list_path, output_folder_name, overwrite):
        self.dataset_path = dataset_path
        self.output_file_list_path = output_file_list_path
        self.output_folder_name = output_folder_name
        self.overwrite = overwrite
        self.csv_file = CsvFile(dataset_path)

    def get_output_filepath(self, original_image_file_path, label):
        filename = path.basename(original_image_file_path)
        filepath = path.abspath(
            path.join('2_preprocess', self.output_folder_name, label, filename))
        return filepath

    def run(self):
        with tf.Session() as sess:
            for train in self.csv_file.read():
                try:
                    image = Image(train[0], int(config.get(
                        CONFIG_SECTION, "IMAGE_SIZE_PX")))
                    label = train[1]

                    to_image_path = self.get_output_filepath(
                        image.file_path, label)
                    print("\nFrom : %s \nTo => %s\n" %
                          (image.file_path, to_image_path))

                    # 新しい訓練用データセットの情報をファイルに書き出し
                    csv = CsvFile(self.output_file_list_path)
                    csv.append(to_image_path + "," + label + "\n")

                    print(path.exists(to_image_path))
                    if self.overwrite == 0 and path.exists(to_image_path):
                        continue

                    image.write(sess, to_image_path)

                except Exception as e:
                    print("Exception!! args:", e.args)
                except:
                    print("All error catch precure!! :")
                    # print(sys.exc_info())
                    import traceback
