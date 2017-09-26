#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import pytumblr
from os import path, pardir
from datetime import datetime, timedelta
from crontab import CronTab
from multiprocessing import Pool

lib_dir = path.abspath(path.join("lib"))
sys.path.append(lib_dir)
import ImageManager
from JobConfig import JobConfig, job_controller
from PhotoRepository import PhotoRepository
from CategorizeResult import CategorizeResult


import configparser
config = configparser.ConfigParser()
config.read(path.abspath(path.join('configs', 'setting.ini')))
CONFIG_SECTION = 'development'


class Tumblr():
    def __init__(self):
        self.photo_repository = PhotoRepository("tumblr")
        self.tumblr_client = pytumblr.TumblrRestClient(
            config.get(CONFIG_SECTION, 'TUMBLR_CONSUMER_KEY'),
            config.get(CONFIG_SECTION, 'TUMBLR_CONSUMER_SECRET'),
            config.get(CONFIG_SECTION, 'TUMBLR_ACCESS_KEY'),
            config.get(CONFIG_SECTION, 'TUMBLR_ACCESS_SECRET')
        )

    def categorize(self, post):
        return [CategorizeResult(
            url=photo["original_size"]["url"],
            filename=ImageManager.get_remote_md5_sum(
                photo["original_size"]["url"])
        ) for idx, photo in enumerate(post["photos"])]

    def download(self, categorize_result):
        ImageManager.download(categorize_result.filepath,
                              categorize_result.url)

    def like(self, post):
        self.tumblr_client.like(post["id"], post["reblog_key"])

    def unlike(self, post):
        self.tumblr_client.unlike(post["id"], post["reblog_key"])

    def includeFappableImage(self, categorized_list):
        labels = [str(categorize_result.label)
                  for idx, categorize_result in enumerate(categorized_list)]
        duplications = set(labels) & set(config.get(
            CONFIG_SECTION, "FAPPABLE_FOLDER").split(","))
        return len(duplications) != 0

    def save(self):
        dashboard_data = self.tumblr_client.dashboard()
        for idx, post in enumerate(dashboard_data["posts"]):
            try:
                if post["type"] == "photo":
                    print(post["id"])
                    if self.photo_repository.identify(post["id"]):
                        continue
                    self.photo_repository.save(post["id"])
                    categorized_list = self.categorize(post)
                    for idx, categorize_result in enumerate(categorized_list):
                        self.download(categorize_result)
                    if self.includeFappableImage(categorized_list):
                        print("like ====> " + categorized_list[0].url)
                        self.like(post)
            except Exception as e:
                print("Exception!! args:", e.args)

    # CAUTION: いちいちlikeを遡ってunlikeするのが面倒なので一週間前の画像ポストは自動unlikeする
    def cleanup(self, blog_name, before):
        print("Before: ", before)
        blog_likes = self.tumblr_client.blog_likes(
            blog_name, limit=20, before=before)
        print(len(blog_likes["liked_posts"]))
        for idx, post in enumerate(blog_likes["liked_posts"]):
            print(post["type"], post["liked_timestamp"],
                  post["id"], post["date"])
            if post["type"] == "photo":
                print("unlike =================> ")
                try:
                    self.unlike(post)
                except Exception as e:
                    print("Unlike Exception args:", e.args)
        if len(blog_likes["liked_posts"]) > 0:
            last_post = blog_likes["liked_posts"][-1]
            # print(blog_likes["liked_posts"][0])
            # print(blog_likes["liked_posts"][-1])
            print(last_post["liked_timestamp"], post["date"])
            self.cleanup(blog_name, before=last_post["liked_timestamp"])


def look_for_fap():
    t = Tumblr()
    t.save()


def cleanup_fap():
    timestamp_oneweek_ago = (
        datetime.now() - timedelta(days=2)).timestamp()
    t = Tumblr()
    t.cleanup(config.get(CONFIG_SECTION, 'TUMBLR_BLOG_NAME'),
              before=int(timestamp_oneweek_ago))


def main():
    cleanup_fap()
    jobConfigs = [
        JobConfig(CronTab("*/15 * * * *"), cleanup_fap),
        JobConfig(CronTab("* * * * *"), look_for_fap)
    ]
    p = Pool(len(jobConfigs))
    try:
        p.map(job_controller, jobConfigs)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
