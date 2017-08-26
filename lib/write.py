#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from urllib.request import urlopen


def write(filename, data):
    csvFile = open(filename, 'wt', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
    try:
        for idx, row in enumerate(data):
            writer.writerow(row)
    finally:
        csvFile.close()
