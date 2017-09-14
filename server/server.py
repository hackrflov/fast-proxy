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

import config as st
from pymongo import MongoClient
host = st.MONGO_HOST
db = st.MONGO_DB
usr = st.MONGO_USERNAME
pwd = st.MONGO_PASSWORD
uri = 'mongodb://{u}:{p}@{h}/{d}'.format(u=usr,p=pwd,h=host,d=db)
client = MongoClient(uri)
clt = client[db][st.MONGO_COLLECTION]

from flask import Flask
app = Flask(__name__)

@app.route('/')
def proxy_list():
    docs = clt.find()
    lt = [doc['ip_port'] for doc in docs]
    dt = { 'status' : 200, 'data' : lt }
    return json.dumps(dt)

@app.route('/fast')
def fast_proxy_list():
    docs = clt.aggregate([
        { '$project': { 'ip_port': 1, 'best': 1, 'rate': { '$divide': [ '$ace_times', { '$add': ['$ace_times', '$bad_times'] } ] } } },
        { '$match': { 'best': { '$lt': 0.5 }, 'rate': { '$gte': 0.9 } } },
    ])
    lt = [doc['ip_port'] for doc in docs]
    dt = { 'status' : 200, 'data' : lt }
    return json.dumps(dt)

@app.route('/best')
def best_proxy_list():
    docs = clt.find().sort('best',1).limit(1)
    lt = [doc['ip_port'] for doc in docs]
    dt = { 'status' : 200, 'data' : lt }
    return json.dumps(dt)

