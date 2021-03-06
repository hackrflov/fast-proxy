#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    File Name: middlewares.py
    Date: 09/13/2017
    Author: hackrflov
    Email: hackrflov@gmail.com
    Python Version: 2.7
"""

import scrapy
import random
import crawler.settings as st

class RandomUserAgentMiddleware(object):

    def process_request(self, request, spider):
        request.headers["User-Agent"] = random.choice(st.USER_AGENTS)

    def process_exception(self, request, exception, spider):
        request.meta['exception'] = exception
        return scrapy.http.Response(url=request.url, request=request, body='Error')

    def process_response(self, request, response, spider):
        if response.status != 200:
            request.meta['exception'] = Exception('StatusError')
            return scrapy.http.Response(url=request.url, request=request, body='Error')
        else:
            return response


