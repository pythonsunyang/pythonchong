# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QianchengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    data_ing = scrapy.Field()
    xueli = scrapy.Field()
    hangwei = scrapy.Field()
    money = scrapy.Field()
    tiem_now = scrapy.Field()
    http_ = scrapy.Field()

    def get_sql(self):
        sql = 'insert into zhaopin_text (title,company,data_ing,xueli,hangwei,money,tiem_now,http_) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        data = (self['title'],self['company'],self['data_ing'],self['xueli'],self['hangwei'],self['money'],self['tiem_now'],self['http_'])
        return (sql,data)