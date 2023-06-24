import datetime
import time
import typing

import schedule
from database import database
from config import Config
from subprocess import PIPE, Popen


class DatabaseDump:
    db = database

    def make_dump(self):
        now_datetime = datetime.datetime.now()
        cmd = f'pg_dump -h {Config.postgres_url.host} -U {Config.postgres_url.user} {Config.postgres_url.path[1:]} > dumps/{Config.postgres_url.path[1:]}__{now_datetime.year}-{now_datetime.month}-{now_datetime.day}__{now_datetime.hour}:{now_datetime.minute}.sql'
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        return p.communicate("{}\n".format(Config.postgres_url.password).encode('utf-8'))

    def run_pending(self):
        self.run_schedule()
        while True:
            schedule.run_pending()
            time.sleep(60)

    def run_schedule(self):
        schedule.every().minute.do(self.make_dump)
