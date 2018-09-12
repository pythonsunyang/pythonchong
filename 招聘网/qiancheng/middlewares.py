# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time
import random
import logging
# from .Proxy_IP_xin import get_ip
from  .kuaiproxy import get_proxy
from scrapy import signals
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from twisted.internet.defer import DeferredLock

class MyRetryMiddleware(RetryMiddleware):

    logger = logging.getLogger(__name__)
    lock = DeferredLock()
    proxy = None
    need_update = True

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        print('我是新写的发送request',self.proxy)
        self.lock.acquire()
        if self.need_update:
            self.proxy = get_proxy()
            print('我的第一个重写的',self.proxy)
            self.need_update = False
        # 在执行完所有的类的属性的操作后, 必须解锁
        #request.meta = {'proxy': self.proxy}
        self.lock.release()
        request.meta['proxy'] = 'http://'+ self.proxy
        return None

    def process_response(self, request, response, spider):
        print(response.text)
        if request.meta.get('dont_retry', False):
            return response
        print('我是新的')
        if response.status in self.retry_http_codes or response.status != 200:
            reason = response_status_message(response.status)
            self.lock.acquire()
            self.proxy = get_proxy()
            print('ip我是重写的', self.proxy)
            self.logger.warning('返回值异常, 进行重试...')
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            # 删除该代理
            self.lock.acquire()
            self.proxy = get_proxy()
            print('ip============================', self.proxy)
            self.logger.warning('连接异常, 进行重试...')
            return self._retry(request, exception, spider)

class QianchengDownloaderMiddleware(object):

    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.lock = DeferredLock()
        self.proxy = None
        self.need_update = True

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s


    def process_request(self, request, spider):

        # Called for each request that goes through the downloader
        # middleware.
        print('我是旧的')
        self.lock.acquire()
        if self.need_update:
            self.proxy = get_proxy()
            print('我的第一个ip',self.proxy)
            self.need_update = False
        # 在执行完所有的类的属性的操作后, 必须解锁
        #request.meta = {'proxy': self.proxy}
        self.lock.release()
        request.meta['proxy'] = 'http://'+ self.proxy



        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # 在之前构造的request中可以加入meta信息dont_retry来决定是否重试
        print(response.text)
        print('我是代理返回的',self.proxy)
        if request.meta.get('dont_retry', False):
            return response
        print(response.status)
        print('我现在返回访问的url',response.url)
        print('我是获取的ip',self.proxy)
        try:
            # Called with the response returned from the downloader.
            if (response.status != 200) or ('login/login.html' in response.url) or  response.status==None:
                print('process_response我换代理ip', response.url)
                self.lock.acquire()
                self.need_update = True
                self.lock.release()
                return request
        except Exception as e:
            print(e)
            self.lock.acquire()
            self.need_update = True
            self.lock.release()
            return request

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        print('我进到exception')
        if exception:
            self.lock.acquire()
            self.need_update = True
            self.lock.release()

        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
