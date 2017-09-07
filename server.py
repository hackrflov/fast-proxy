#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    File Name: proxy_list.py
    Date: 09/07/2017
    Author: hackrflov
    Email: hackrflov@gmail.com
    Python Version: 2.7
"""

import json

from config import MONGO_SETTINGS
from pymongo import MongoClient
host = MONGO_SETTINGS.get('MONGO_HOST')
db = MONGO_SETTINGS.get('MONGO_DB')
usr = MONGO_SETTINGS.get('MONGO_USERNAME')
pwd = MONGO_SETTINGS.get('MONGO_PASSWORD')
uri = 'mongodb://{u}:{p}@{h}/{d}'.format(u=usr,p=pwd,h=host,d=db)
client = MongoClient(uri)
db = client[db]

from flask import Flask
app = Flask(__name__)

@app.route('/')
def proxy_list():
    docs = db.proxy.find()
    lt = [doc['ip_port'] for doc in docs]
    dt = { 'status' : 200, 'data' : lt }
    return json.dumps(dt)

