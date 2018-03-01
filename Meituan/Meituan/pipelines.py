

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import demjson
from pymongo import MongoClient
from scrapy.conf import settings


class MeituanPipeline(object):
    def __init__(self):
        self.f = open('meituan.json', 'w', encoding='UTF-8')
        # self.f = open('meituan.json', 'w')
        # self.f = open('meituan_xixi.json', 'w', encoding='UTF-8')

    def process_item(self, item, spider):
        print('start json')
        # str_data = demjson.encode(dict(item)) + ',\n'

        str_data = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        print(type(str_data))
        # 打印正常, 保存json时中文变成\u751F\u5316\u5371\u673A字符(Unicode),
        # python3以上取消了decode，所以你直接想st.decode(“utf-8”)的话会报str没有decode方法的错
        # 解决方法如下
        # self.f.write(str_data.encode('utf-8').decode('unicode_escape'))
        self.f.write(str_data)
        print('end json')
        return item

    def __del__(self):
        self.f.close()

class MeituanMongoPipeline(object):
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
        print('start mongodb')
        # str_data = demjson.encode(dict(item))

        str_data = json.dumps(dict(item), ensure_ascii=False)
        # new_data = str_data.encode('utf-8').decode('unicode_escape')
        print(type(str_data))
        dict_data = demjson.decode(str_data)
        # dict_data = json.loads(new_data)
        # print(dict_data)
        # 插入数据
        self.col.insert(dict_data)
        print('end mongodb')
        return item


    def __del__(self):
        self.client.close()
