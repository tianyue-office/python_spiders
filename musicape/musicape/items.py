# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MusicapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 歌手名
    singer = scrapy.Field()
    # 歌曲名
    sname = scrapy.Field()
    # 歌曲下载链接
    down_link = scrapy.Field()
    # 歌曲下载密码
    down_pwd = scrapy.Field()
    # 歌曲专辑
    salbum = scrapy.Field()
    # 歌曲大小
    ssize = scrapy.Field()
    # 歌曲发布时间
    stime = scrapy.Field()
    # 歌曲语言
    slanguage = scrapy.Field()
    pass



