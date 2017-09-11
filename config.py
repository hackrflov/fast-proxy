#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    File Name: config.py
    Date: 09/07/2017
    Author: hackrflov
    Email: hackrflov@gmail.com
    Python Version: 2.7
"""

# 利用一个正则就可以直接采集代理IP的站点
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
    'proxy_regx': r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,4}"
}

# 需要利用xpath 定位代理IP 的站点
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

# 需要分行处理的TXT格式
PROXY_SITES_BY_TXT = [
    {
        'urls' : ['https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'],
        'ip_path' : 'host',
        'port_path' : 'port'
    },
]

# User-Agent list
USER_AGENT_LIST = [
    'Mozilla/4.0 (compatible; MSIE 5.0; SunOS 5.10 sun4u; X11)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser;',
    'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
    'Microsoft Internet Explorer/4.0b1 (Windows 95)',
    'Opera/8.00 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)',
    'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; ZoomSpider.net bot; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; QihooBot 1.0 qihoobot@qihoo.net)',
]


# 爬代理超时时间
CRAWL_TIMEOUT = 10

# 测试代理超时时间
TEST_TIMEOUT = 0.50

#重试次数
RETRY_NUM = 1

# 目标URL
TARGET_URL = "http://api.bilibili.com/x/v2/fav/video?vmid=32312072&fid=30423962"

# 数据库
MONGO_SETTINGS = {
    'MONGO_HOST' : '127.0.0.1',  # set x.x.x.x for remote access
    'MONGO_DB' : 'proxy',  # default collection name
    'MONGO_USERNAME' : 'default',  # for auth
    'MONGO_PASSWORD' : 'default',  # for auth
}






