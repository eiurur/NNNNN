#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path
import http
import tweepy
from tweepy.auth import OAuthHandler
from tweepy.api import API
from types import *

lib_dir = path.abspath(path.join("lib"))
sys.path.append(lib_dir)
import ImageManager
from PhotoRepository import PhotoRepository
from CategorizeResult import CategorizeResult

import configparser
config = configparser.ConfigParser()
config.read(path.abspath(path.join('configs', 'setting.ini')))
CONFIG_SECTION = 'development'


class myExeption(Exception):
    pass


class StreamListener(tweepy.streaming.StreamListener):

    def __init__(self):
        # データベースに接続するときに使用
        # ↓これを忘れると動かない
        super(StreamListener, self).__init__()
        self.photo_repository = PhotoRepository("twitter")

    def __del__(self):
        # データベースを閉じるときに使用
        print("DEL")

    def get_tweet(self, status):
        return status.retweeted_status if hasattr(status, 'retweeted_status') else status

    def save(self, media):
        category_reuslt = CategorizeResult(
            url=media['media_url'],
            filename=media['media_url'].split("/")[-1]
        )
        ImageManager.download(category_reuslt.filepath, category_reuslt.url)

    def on_status(self, status):
        tweet = self.get_tweet(status)
        if self.photo_repository.identify(tweet.id_str):
            return
        self.photo_repository.save(tweet.id_str)
        if hasattr(tweet, "extended_entities") and 'media' in tweet.extended_entities and len(tweet.extended_entities['media']):
            for media in tweet.extended_entities['media']:
                self.save(media)
        return True

    def on_error(self, status):
        print("can't get")
        raise myExeption


def get_oauth():
    consumer_key = config.get(CONFIG_SECTION, 'TWITTER_CONSUMER_KEY')
    consumer_secret = config.get(CONFIG_SECTION, 'TWITTER_CONSUMER_SECRET')
    access_key = config.get(CONFIG_SECTION, 'TWITTER_ACCESS_KEY')
    access_secret = config.get(CONFIG_SECTION, 'TWITTER_ACCESS_SECRET')
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return auth


def getListMembers(api, my_info, list_name):
    list_members = []
    for member in tweepy.Cursor(api.list_members, owner_screen_name=my_info.screen_name, slug=list_name).items():
        list_members.append(member.id_str)
    return list_members


if __name__ == '__main__':
    auth = get_oauth()
    api = tweepy.API(auth)
    my_info = api.me()
    stream = tweepy.Stream(auth, StreamListener())
    while True:
        try:
            stream.filter(languages=['ja'], follow=getListMembers(
                api, my_info, config.get(CONFIG_SECTION, 'TWITTER_STREAING_LIST_NAME')))
        except http.client.IncompleteRead:
            # https://stackoverflow.com/questions/28717249/error-while-fetching-tweets-with-tweepy
            # Oh well, reconnect and keep trucking
            continue
        except KeyboardInterrupt:
            # Or however you want to exit this loop
            stream.disconnect()
            break
        except:
            print("What happend!!")
            print(sys.exc_info())
            import traceback

            # #twitterに弾かれた場合は少し待って接続し直す
            # stream = tweepy.Stream(auth,StreamListener())
