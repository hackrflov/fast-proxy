#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    File Name: proxyspider.py
    Date: 09/07/2017
    Author: hackrflov
    Email: hackrflov@gmail.com
    Python Version: 2.7
"""


import requests
import Queue
import re
import json
from lxml import html
from random import choice
import threading
from threading import Timer
import time
import urllib3
import pdb
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from pymongo import MongoClient
import logging
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger('proxyspider')
log.setLevel('INFO')

from config import (
    PROXY_SITES_BY_REGX, PROXY_SITES_BY_XPATH, PROXY_SITES_BY_TXT, USER_AGENT_LIST, RETRY_NUM, CRAWL_TIMEOUT, TEST_TIMEOUT, TARGET_URL, MONGO_SETTINGS
)

class ProxySpider(object):

    def __init__(self):
        self.proxy_queue = Queue.Queue()
        self.fetch_finish = False
        host = MONGO_SETTINGS.get('MONGO_HOST')
        db = MONGO_SETTINGS.get('MONGO_DB')
        usr = MONGO_SETTINGS.get('MONGO_USERNAME')
        pwd = MONGO_SETTINGS.get('MONGO_PASSWORD')
        uri = 'mongodb://{u}:{p}@{h}/{d}'.format(u=usr,p=pwd,h=host,d=db)
        client = MongoClient(uri)
        self.db = client[db]

    """
       起一个线程将采集到的所有代理IP写入一个queue中
    """
    def fetch_proxy(self):
        '''根据正则直接获取代理IP 部分'''
        for site in PROXY_SITES_BY_REGX['urls']:
            log.info('Fetching {}'.format(site))
            resp  = self._fetch(site)
            if resp is not None and resp.status_code == 200:
                try:
                    proxy_list = self._extract_by_regx(resp)
                    for proxy in proxy_list:
                        log.debug("Get proxy {} and push into queue".format(proxy))
                        self.proxy_queue.put(proxy)
                except Exception as e:
                    continue
        '''根据xpath 获取代理IP 部分'''
        for sites in PROXY_SITES_BY_XPATH:
            log.info('Fetching {}'.format(sites['urls'][0]))
            for site in sites['urls']:
                resp  = self._fetch(site)
                if resp is not None and resp.status_code == 200:
                    try:
                        proxy_list = self._extract_by_xpath(resp, sites['ip_xpath'], sites['port_xpath'])
                        for proxy in proxy_list:
                            log.debug('Get proxy {} and push into queue'.format(proxy))
                            self.proxy_queue.put(proxy)
                    except Exception as e:
                        continue
        '''根据txt 获取代理IP 部分'''
        for sites in PROXY_SITES_BY_TXT:
            log.info('Fetching {}'.format(sites['urls'][0]))
            for site in sites['urls']:
                resp = self._fetch(site)
                pdb.set_trace()
                if resp is not None and resp.status_code == 200:
                    try:
                        data = resp.text.split('\n')
                        for msg in data[:-1]:
                            msg = json.loads(msg)
                            proxy = 'http://{host}:{port}'.format(host=msg[sites['ip_path']], port=msg[sites['port_path']])
                            log.debug('Get proxy {} and push into queue'.format(proxy))
                            self.proxy_queue.put(proxy)
                            print self.proxy_queue
                    except Exception as e:
                        continue
        log.info("Get all proxy in queue!")
        self.fetch_finish = True

        # 下一次执行在5分钟之后
        Timer(300, self.fetch_proxy, ()).start()
        Timer(300, self.test_proxy, ()).start()
        Timer(300, self.test_proxy, ()).start()
        log.info("Get all proxy in queue!")
        self.fetch_finish = True

        # 下一次执行在5分钟之后
        Timer(300, self.fetch_proxy, ()).start()
        Timer(300, self.test_proxy, ()).start()
        Timer(300, self.test_proxy, ()).start()

    """
        起多个线程取出queue中的代理IP 测试是否可用
    """
    def test_proxy(self):

        while not self.proxy_queue.empty() or self.fetch_finish == False:
            log.debug("Begin to TEST proxy from queue")
            proxy = self.proxy_queue.get()
            # 访问国内网站，获取速度
            try:
                req = self._fetch(TARGET_URL, proxy)
                sec = req.elapsed.total_seconds()
                log.info('{p} use {s} seconds'.format(p=proxy,s=sec))
                if sec < TEST_TIMEOUT:  # 访问速度
                    pd = {'ip_port': proxy, 'time': sec}
                    self.insert_into_db(pd)
                    log.info('Insert proxy {} into db'.format(pd))
            except Exception as e:
                log.debug('use {p} concur error {e}'.format(p=proxy,e=e))

    """
        起一个线程遍历检测所有数据库中的代理IP，修改状态
    """
    def update_proxy(self):
        while True:
            log.info('Before refresh: having {} proxies'.format(self.db.proxy.count()))
            docs = self.db.proxy.find()
            docs = [doc for doc in docs]
            req = self._fetch(TARGET_URL, doc['ip_port'])
            for doc in docs:
                try:
                    ip_port = doc['ip_port']
                    req = self._fetch(TARGET_URL, ip_port)
                    sec = req.elapsed.total_seconds()
                except:
                    self.db.proxy.delete_one({'ip_port': ip_port})
                    continue
                log.info('==== UPDATING ==== {p} use {s} seconds'.format(p=ip_port,s=sec))
                if sec >= TEST_TIMEOUT:
                    self.db.proxy.delete_one({'ip_port': ip_port})
                else:
                    self.db.proxy.update_one({ 'ip_port': ip_port }, { '$set' : doc }, upsert=True)
            log.info('After refresh: having {} proxies'.format(self.db.proxy.count()))

    """ 将代理插入数据库中 """
    def insert_into_db(self, pd):
        ip_port = pd['ip_port']
        try:
            self.db.proxy.update_one({ 'ip_port': ip_port }, { '$set': pd }, upsert=True)
            log.info('Successfully upsert {}'.format(ip_port))
        except Exception as error:
            log.error('Upsert {p} error, detail: {e}'.format(p=ip_port,e=error))

    """ 抓取代理网站函数"""
    def _fetch(self, url, proxy=None):
        timeout = CRAWL_TIMEOUT if proxy is None else TEST_TIMEOUT
        kwargs = {
            "headers": {
                "User-Agent": choice(USER_AGENT_LIST),
            },
            "timeout": timeout,
            "verify": False,
        }
        resp = None
        for i in range(RETRY_NUM):
            try:
                if proxy is not None:
                    kwargs["proxies"] = {
                            "http": proxy}
                resp = requests.get(url, **kwargs)
                break
            except Exception as e:
                log.debug("fetch %s  failed!\n%s , retry %d" % (url, str(e), i+1))
                pass
        return resp

    """ 根据解析抓取到的内容，得到代理IP"""
    def _extract_by_regx(self, resp):
        proxy_list = []
        if resp is not None:
            proxy_list = re.findall(PROXY_SITES_BY_REGX['proxy_regx'], resp.text)
        return proxy_list

    def _extract_by_xpath(self, resp, ip_xpath, port_xpath):
        proxy_list = []
        if resp is not None:
            resp = html.fromstring(resp.text)
            ip_list = resp.xpath(ip_xpath)
            ip_list = [ip for ip in ip_list if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',ip)]
            port_list = resp.xpath(port_xpath)
            for i in range(len(ip_list)):
                proxy = ip_list[i] + ":" + port_list[i]
                proxy_list.append(proxy)
        return proxy_list

    """
    抓取线程: 5分钟一次 单线程
    测试线程: 5分钟一次 双线程
    刷新线程: 不间断 单线程
    """
    def run(self):
        Timer(1, self.fetch_proxy, ()).start()
        Timer(1, self.test_proxy, ()).start()
        Timer(1, self.test_proxy, ()).start()
        Timer(60, self.update_proxy, ()).start()

def main():
    spider = ProxySpider()
    spider.run()
    #spider.fetch_proxy()
    #url = 'https://api.bilibili.com/x/v2/fav/video?vmid=11&fid=1224795'
    #spider._fetch(TARGET_URL, '61.135.217.7:80')
    #spider.update_proxy()

if __name__ == "__main__":
    main()

