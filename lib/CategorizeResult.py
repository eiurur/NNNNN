#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path
from classify import classify


class CategorizeResult():
    def __init__(self, url, filename):
        classifying_result = classify([url])
        self.label = classifying_result[1]
        self.url = url
        self.filename = "{}.jpg".format(filename)
        self.filepath = "{}/{}/{}".format(
            path.abspath(path.join('4_collect', 'images')), self.label, self.filename)
