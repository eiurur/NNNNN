#!/usr/bin/env python
# -*- coding: utf-8 -*-


class File(object):
    def __init__(self, path):
        self.path = path

    def append(self, text):
        with open(self.path, "a") as f:
            f.write(str(text))
