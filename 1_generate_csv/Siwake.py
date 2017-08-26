#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import glob


class Siwake:
    def __init__(self, filepath, separator=" "):
        self.output_filepath = filepath
        self.separator = separator
        self.store = []
        self.dataset = []

    def load(self, dataset):
        self.dataset = dataset
        for data in dataset:
            files = glob.glob(data["directory"] + "/*")
            lines = [os.path.abspath(
                file + self.separator + data["label"]) for file in files]
            self.store.extend(lines)

    def write(self):
        with open(self.output_filepath, "w") as f:
            for item in self.store:
                f.write("{}\n".format(item))
