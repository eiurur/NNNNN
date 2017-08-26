#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient


class MongoClientProvider:
    def __init__(self):
        self.client = MongoClient('127.0.0.1', 27017)
        self.db = ''

    def switch_database_to(self, database_name):
        self.db = self.client[database_name]

    def find(self, collection_name, query={}, options={}):
        return self.db[collection_name].find(query, options)

    def count(self, collection_name, query={}):
        return self.db[collection_name].count(query)

    def upsert(self, collection_name, query={}, options={}):
        return self.db[collection_name].update(query, options, upsert=True)
