# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from qiancheng.my_mysql import my_sql
class QianchengPipeline(object):
    def process_item(self, item, spider):
        Mysql = my_sql()
        # print(item)
        sql,data = item.get_sql()
        Mysql.mysql_sql(sql,data)