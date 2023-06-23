from celery import Celery
import json
import os
from database import Base

celery = Celery('tasks', broker='redis://localhost:6739')

# @celery.task
# def json_db_dump(dump_file):

#     # db = тут импорт базы данных
#     data = {}
#     json_file = 'db.json'

#     with open(json_file, 'w') as file:
#         json.dump(data, json_file)

#     return json_file