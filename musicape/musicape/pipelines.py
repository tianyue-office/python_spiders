# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.conf import settings


class MusicapePipeline(object):
    def __init__(self):
        host = settings['MONGO_HOST']
        port = settings['MONGO_PORT']
        dbname = settings['MONGO_DBNAME']
        colname = settings['MONGO_COLNAME']

        # 创建数据库链接
        self.client = MongoClient(host, port)
        # 选择数据库
        self.db = self.client[dbname]
        # 选择集合
        self.col = self.db[colname]

    def process_item(self, item, spider):
        # 插入数据
        self.col.insert(dict(item))
        return item

    def __del__(self):
        self.client.close()
