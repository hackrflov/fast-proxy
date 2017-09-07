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
        'https://www.rmccurdy.com/scripts/proxy/good.txt',
        'http://www.proxylists.net/?HTTP',
    ],
    'proxy_regx': r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,4}"
}

# 需要利用xpath 定位代理IP 的站点
PROXY_SITES_BY_XPATH = [
    {
        'urls': ['http://www.66ip.cn/{}.html'.format(pn) for pn in range(1, 11)],
        'ip_xpath': ".//*[@id='main']/div/div[1]/table/tr[position()>1]/td[1]/text()" ,
        'port_xpath': ".//*[@id='main']/div/div[1]/table/tr[position()>1]/td[2]/text()"
    },
    {
        'urls': ['http://www.mimiip.com/gngao/{}'.format(pn) for pn in range(1, 11)],
        'ip_xpath': ".//table[@class='list']/tbody/tr/td[1]/text()",
        'port_xpath': ".//table[@class='list']/tbody/tr/td[2]/text()"
    },
    {
        'urls' : ['http://www.xicidaili.com/nn/{}'.format(pn) for pn in range(1,11)],
        'ip_xpath' : '//table[@id="ip_list"]//tr[position()>1]/td[position()=2]/text()',
        'port_xpath' : '//table[@id="ip_list"]//tr[position()>1]/td[position()=3]/text()'
    },
    {
        'urls' : ['http://www.kuaidaili.com/free/inha/{}/'.format(pn) for pn in range(1,11)],
        'ip_xpath' : '//td[@data-title="IP"]/text()',
        'port_xpath' : '//td[@data-title="PORT"]/text()'
    },
]

CHECK_PROXY_XPATH = {
    "HTTP_VIA": ".//li[@class='proxdata'][1]/span/text()",
    "HTTP_X_FORWARDED_FOR": ".//li[@class='proxdata'][2]/span/text()"
}

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


# 超时时间
TIME_OUT = 4

#重试次数
RETRY_NUM = 3

#代理最慢时间限制
PROXY_TIME_LIMIT = 0.20

# 目标URL
TARGET_URL = "https://api.bilibili.com/x/v2/fav/video?vmid=32312072&fid=30423962"

# 数据库
MONGO_SETTINGS = {
    'MONGO_HOST' : '127.0.0.1',  # set x.x.x.x for remote access
    'MONGO_DB' : 'proxy',  # default collection name
    'MONGO_USERNAME' : 'default',  # for auth
    'MONGO_PASSWORD' : 'default',  # for auth
}






