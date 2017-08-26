#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import math
import time


class JobConfig():
    def __init__(self, crontab, job):
        self._crontab = crontab
        self.job = job

    def schedule(self):
        crontab = self._crontab
        return datetime.now() + timedelta(seconds=math.ceil(crontab.next()))

    def next(self):
        crontab = self._crontab
        return math.ceil(crontab.next())


def job_controller(jobConfig):
    while True:
        try:
            time.sleep(jobConfig.next())
            jobConfig.job()
        except KeyboardInterrupt:
            break
