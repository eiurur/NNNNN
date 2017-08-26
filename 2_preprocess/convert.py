#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

from TrainingImageConverter import TrainingImageConverter

# images filepathes and labels
TRAIN_DATASET_PATH = os.path.abspath(
    os.path.join('1_generate_csv', 'train.txt'))
TEST_DATASET_PATH = os.path.abspath(os.path.join('1_generate_csv', 'test.txt'))

# train data for training
TRAIN_DATA_PATH = os.path.abspath(
    os.path.join('3_train', 'training', 'train.txt'))
# train data for test
TEST_DATA_PATH = os.path.abspath(
    os.path.join('3_train', 'training', 'test.txt'))


def preprocessinog(output_path):
    if os.path.exists(output_path):
        os.remove(output_path)


if __name__ == '__main__':
    print(sys.argv)
    print("{}.\n{}.\n{}.\n{}.\n".format(
          TRAIN_DATASET_PATH,
          TEST_DATASET_PATH,
          TRAIN_DATA_PATH,
          TEST_DATA_PATH)
          )

    input_path = TEST_DATASET_PATH if '--test_image' in sys.argv else TRAIN_DATASET_PATH
    output_path = TEST_DATA_PATH if '--test_image' in sys.argv else TRAIN_DATA_PATH
    preprocessinog(output_path)

    output_folder_name = 'test_images' if '--test_image' in sys.argv else 'images'
    overwrite = 1 if '--overwrite' in sys.argv else 0

    converter = TrainingImageConverter(
        input_path, output_path, output_folder_name, overwrite)
    converter.run()
