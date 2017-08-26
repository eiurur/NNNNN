#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
from File import File


class CsvFile(File):
    def __init__(self, path):
        super().__init__(path)

    def read(self):
        list = []
        with open(self.path, 'r') as file:
            # return [elem[0].split(',') for elem in csv.reader(file, delimiter='\n')]
            for elem in csv.reader(file, delimiter='\n'):
                list.append(elem[0].split(','))
        return list
