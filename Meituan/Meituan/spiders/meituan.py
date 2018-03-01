
import json

import re
import datetime
import demjson
import requests
import scrapy
from scrapy.conf import settings

from Meituan.items import MeituanItem
# ----1.导入类
from scrapy_redis.spiders import RedisSpider

# ----2.修改类的继承
# class MeituanSpider(scrapy.Spider):
class MeituanSpider(RedisSpider):
    '''美团杭州美食, 默认排序'''

    name = 'meituan'
    # allowed_domains = ['meituan.com']
    base_url = 'http://hz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%9D%AD%E5%B7%9E&page='

    page = 1
    start_urls = [base_url + str(page)]
    # ----4.设置redis_key获取起始的url
    # redis_key = ''

    # ----5 设置动态获取允许的域
    def __init__(self, *args, **kwargs):
        self.start = datetime.datetime.now()
        print(self.start)
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        # print('------', self.allowed_domains)
        super(MeituanSpider, self).__init__(*args, **kwargs)

    def __del__(self):
        end = datetime.datetime.now()
        print(end)
        print((end - self.start).seconds)

    def parse(self, response):

        # 获取每个美食节点列表
        node_list = list()
        try:
            node_list = json.loads(response.body)['data']['poiInfos']
        except:
            self.page += 1
            next_url = self.base_url + str(self.page)
            yield scrapy.Request(next_url, callback=self.parse)

        for node in node_list:

            item = MeituanItem()

            item['id'] = node['poiId']
            # print(item['id'])
            item['title'] = node['title']
            # print(node['title'])
            item['shop_link'] = 'http://www.meituan.com/meishi/' + str(item['id'])
            item['shop_img_link'] = node['frontImg']
            item['address'] = node['address']
            # print(node['address'])
            item['score'] = node['avgScore']
            item['comment_num'] = node['allCommentNum']
            item['price_avg'] = node['avgPrice']
            # print(item)
            # yield item
            yield scrapy.Request(
                item['shop_link'],
                callback=self.parse_detail,
                meta={'meta1': item}
            )

        if len(node_list):
            self.page += 1
            next_url = self.base_url + str(self.page)
            yield scrapy.Request(next_url, callback=self.parse)


    def parse_detail(self, response):
        item = response.meta['meta1']
        data = response.xpath('/html/body/script/text()').extract()[2]
        data_list = re.findall(r'"phone":"(.*)","openTime":"(.*)","extraInfos":', data)
        item['tel'] = data_list[0][0]
        item['open_time'] = data_list[0][1]
        # http://www.meituan.com/meishi/api/poi/getMerchantComment?id=item['id']&offset={}&pageSize=800&sortType=1
        comment_list = list()
        url = 'http://www.meituan.com/meishi/api/poi/getMerchantComment?id=' + str(item['id']) + '&offset={}&pageSize=500&sortType=1'
        headers = {
            'User-Agent': settings['USER_AGENT']
        }
        num = 0
        while True:

            resp = requests.get(url.format(num), headers=headers)
            # print(resp.content)
            try:
                resp_dict = demjson.decode(resp.content)
            except:
                continue
            # resp_dict = json.loads(resp.content)
            comments = resp_dict['data']['comments']
            # print(comments)
            if not comments:
                break
            for com in comments:
                temp = dict()
                temp['uname'] = com['userName']
                temp['uid'] = com['userId']
                temp['comment'] = com['comment']
                comment_list.append(temp)
            print(len(comments),',',len(comment_list))
            num += 500
        print('-' * 30, len(comment_list))
        item['comment_list'] = comment_list
        print('=' * 30, len(item))

        yield item



