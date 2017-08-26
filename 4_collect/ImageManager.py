#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from urllib.request import urlopen
import cv2
import hashlib
import os


def get_remote_md5_sum(url, max_file_size=100 * 1024 * 1024):
    resp = urlopen(url)
    hash = hashlib.md5()

    total_read = 0
    while True:
        data = resp.read(4096)
        total_read += 4096

        if not data or total_read > max_file_size:
            break

        hash.update(data)

    return hash.hexdigest()


def url_to_image(url):
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def download(dst_filpath, url):
    cv2.imwrite(dst_filpath, url_to_image(url))
