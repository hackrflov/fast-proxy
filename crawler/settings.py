#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    File Name: settings.py
    Date: 09/13/2017
    Author: hackrflov
    Email: hackrflov@gmail.com
    Python Version: 2.7
"""

BOT_NAME = 'proxy'

SPIDER_MODULES = ['crawler']

# Log level: DEBUG | INFO | WARNING | ERROR
LOG_LEVEL = 'INFO'

# Enable cookies
COOKIES_ENABLED = False

# Enable redirect: 302
REDIRECT_ENABLED = False

# Enable retry when failed
RETRY_ENABLED = False

# Max requests at the same time
CONCURRENT_REQUESTS = 4

# Custom MongoDB connection
MONGO_HOST = '127.0.0.1'  # set x.x.x.x for remote access
MONGO_DB = 'proxy'  # default db name
MONGO_COLLECTION = 'proxy'  # default collection name
MONGO_USERNAME = 'default'  # for auth
MONGO_PASSWORD = 'default'  # for auth

# Custom and default middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 555,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'crawler.middlewares.RandomUserAgentMiddleware': 532
}

# Wait time after each fetch round
FETCH_INTERVAL = 300

# Wait time after each update round
UPDATE_INTERVAL = 2

# Download timeout for fetching proxies
CRAWL_TIMEOUT = 300

# Download Timeout
DOWNLOAD_TIMEOUT = 0.5

# Max response time for each proxy
PROXY_LIMIT_LATENCY = 0.5

# Url for proxy testing
TEST_URL = "http://api.bilibili.com/x/v2/fav/video?vmid=32312072&fid=30423962"

# Proxy sources support parsing with regx
PROXY_SITES_BY_REGX = {
    'urls': [
        'http://ab57.ru/downloads/proxyold.txt',
        'http://www.proxylists.net/http_highanon.txt',
        'http://www.proxylists.net/?HTTP',
        'https://www.rmccurdy.com/scripts/proxy/good.txt',
        'http://www.site-digger.com/html/articles/20110516/proxieslist.html',
        'http://ip.baizhongsou.com',
        'https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt',
        'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt',
    ],
}
PROXY_REGX = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,4}"

# Proxy sources support parsing with xpath
PROXY_SITES_BY_XPATH = [
    {
        'urls': ['http://www.66ip.cn/{}.html'.format(pn) for pn in range(1,21)],
        'ip_xpath': ".//*[@id='main']/div/div[1]/table/tr[position()>1]/td[1]/text()" ,
        'port_xpath': ".//*[@id='main']/div/div[1]/table/tr[position()>1]/td[2]/text()"
    },
    {
        'urls': ['http://www.mimiip.com/gngao/{}'.format(pn) for pn in range(1,21)],
        'ip_xpath': ".//table[@class='list']/tbody/tr/td[1]/text()",
        'port_xpath': ".//table[@class='list']/tbody/tr/td[2]/text()"
    },
    {
        'urls' : ['http://www.xicidaili.com/nn/{}'.format(pn) for pn in range(1,21)],
        'ip_xpath' : '//table[@id="ip_list"]//tr[position()>1]/td[position()=2]/text()',
        'port_xpath' : '//table[@id="ip_list"]//tr[position()>1]/td[position()=3]/text()'
    },
    {
        'urls' : ['http://www.kuaidaili.com/free/inha/{}/'.format(pn) for pn in range(1,21)],
        'ip_xpath' : '//td[@data-title="IP"]/text()',
        'port_xpath' : '//td[@data-title="PORT"]/text()'
    },
    {
        'urls' : ['http://proxysockslist.com/proxy-in-CHINA-page-1'],
        'ip_xpath' : '//tr/*[1]/text()',
        'port_xpath' : '//tr/*[2]/text()'
    },
    {
        'urls' : ['https://free-proxy-list.com/?page={}'.format(pn) for pn in range(1,6)],
        'ip_xpath' : '//tr/*[1]/a/text()',
        'port_xpath' : '//tr/*[3]/text()'
    },
    {
        'urls' : ['http://www.kxdaili.com/dailiip/1/{}.html#ip'.format(pn) for pn in range(1,11)],
        'ip_xpath' : '//tr/*[1]/text()',
        'port_xpath' : '//tr/*[2]/text()'
    },
]

# Proxy sources in txt format
PROXY_SITES_BY_TXT = [
    {
        'urls' : ['https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'],
        'ip_key' : 'host',
        'port_key' : 'port'
    },
]

# User-Agent list
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
