#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MongoClientProvider import MongoClientProvider


class PhotoRepository(object):
    def __init__(self, service_name):
        self.mongo_client = MongoClientProvider()
        self.mongo_client.switch_database_to('NNNNN')
        self.service_name = service_name

    def save(self, id):
        self.mongo_client.upsert(
            collection_name=self.service_name, query={"id_str": id}, options={"id_str": id})

    def identify(self, id):
        same_post_count = self.mongo_client.count(
            collection_name=self.service_name, query={"id_str": id})
        return same_post_count != 0
