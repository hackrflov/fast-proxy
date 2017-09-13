#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    File Name: proxy_spider.py
    Date: 09/13/2017
    Author: hackrflov
    Email: hackrflov@gmail.com
    Python Version: 2.7
"""


import re
import json
import time
import logging
log = logging.getLogger('scrapy.spider')
from lxml import html
from datetime import datetime, timedelta

import scrapy
import crawler.settings as st
from pymongo import MongoClient

class ProxySpider(scrapy.Spider):

    name = 'proxy'

    def __init__(self, *args, **kwargs):
        super(ProxySpider, self).__init__(*args, **kwargs)
        self.connect()

    def connect(self):
        log.info('Connecting to MongoDB...')
        host = st.MONGO_HOST
        db = st.MONGO_DB
        usr = st.MONGO_USERNAME
        pwd = st.MONGO_PASSWORD
        if usr and pwd:
            uri = 'mongodb://{u}:{p}@{h}/{d}'.format(u=usr,p=pwd,h=host,d=db)
        else:
            uri = 'mongodb://{h}/{d}'.format(h=host,d=db)
        client = MongoClient(uri)
        self.clt = client[db][st.MONGO_COLLECTION]

    def start_requests(self):
        while True:
            log.info('Start to fetch proxy...')
            meta = {'download_timeout': st.CRAWL_TIMEOUT}

            for url in st.PROXY_SITES_BY_REGX['urls']:
                yield scrapy.Request(url=url, meta=meta, callback=self.parse_regx)

            for site in st.PROXY_SITES_BY_XPATH:
                meta['ip_xpath'] = site['ip_xpath']
                meta['port_xpath'] = site['port_xpath']
                yield scrapy.Request(url=url, meta=meta, callback=self.parse_xpath)

            for site in st.PROXY_SITES_BY_TXT:
                meta['ip_key'] = site['ip_key']
                meta['port_key'] = site['port_key']
                yield scrapy.Request(url=url, meta=meta, callback=self.parse_txt)

            log.info('Fetching is finished, waiting for parsing...')
            time.sleep(10)
            last_dt = datetime.now()

            log.info('Start to update proxy...')
            while True:
                cur_dt = datetime.now()
                if cur_dt - last_dt >= timedelta(seconds=st.FETCH_INTERVAL):  # should restart fecthing now
                    last_dt = cur_dt
                    break
                else:
                    log.info('Before refresh: having {} proxies'.format(self.clt.count()))
                    docs = self.clt.find()
                    for doc in docs:
                        meta = {'proxy': 'http://{}'.format(doc['ip_port']) }
                        yield scrapy.Request(url=st.TEST_URL, meta=meta, dont_filter=True, callback=self.parse_test)
                        log.debug('Testing [{}]...'.format(doc['ip_port']))

                    log.info('All update requests have been send, waiting for parsing...')
                    interval = st.UPDATE_INTERVAL if self.clt.count() >= 15 else 30
                    time.sleep(interval)

    def parse_regx(self, response):
        proxy_list = re.findall(st.PROXY_REGX, response.body)
        for ip_port in proxy_list:
            meta = {'proxy': 'http://{}'.format(ip_port) }
            yield scrapy.Request(url=st.TEST_URL, meta=meta, dont_filter=True, callback=self.parse_test)
            log.debug('Testing [{}]...'.format(ip_port))

    def parse_xpath(self, response):
        r = html.fromstring(response.body)
        ip_list = r.xpath(response.meta['ip_xpath'])
        ip_list = [ip for ip in ip_list if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',ip)]
        port_list = r.xpath(response.meta['port_xpath'])
        for i in range(len(ip_list)):
            ip_port = ip_list[i] + ":" + port_list[i]
            meta = {'proxy': 'http://{}'.format(ip_port) }
            yield scrapy.Request(url=st.TEST_URL, meta=meta, dont_filter=True, callback=self.parse_test)
            log.debug('Testing [{}]...'.format(ip_port))

    def parse_txt(self, response):
        data = resp.text.split('\n')
        for msg in data[:-1]:
            msg = json.loads(msg)
            ip = msg[response.meta['ip_key']]
            port = msg[response.meta['port_key']]
            ip_port = '{ip}:{port}'.format(ip=ip, port=port)
            meta = {'proxy': 'http://{}'.format(ip_port) }
            yield scrapy.Request(url=st.TEST_URL, meta=meta, dont_filter=True, callback=self.parse_test)
            log.debug('Testing [{}]...'.format(ip_port))

    def parse_test(self, response):
        try:
            ip_port = re.sub('http://', '', response.meta['proxy'])
            data = json.loads(response.body)['data']['fid']
            seconds = response.request.meta['download_latency']
            if seconds >= st.PROXY_LIMIT_LATENCY:
                raise Exception
            else:
                log.info('Insert proxy {p}, used {s} seconds'.format(p=ip_port, s=seconds))
                proxy = { 'ip_port': ip_port, 'seconds': seconds }
                self.clt.update_one({ 'ip_port': ip_port }, { '$set': proxy }, upsert=True)
        except:
            log.info('Delete bad proxy: {}'.format(ip_port))
            self.clt.delete_one({'ip_port': ip_port})








