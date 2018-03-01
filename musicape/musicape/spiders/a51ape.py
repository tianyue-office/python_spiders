# -*- coding: utf-8 -*-
import re
import scrapy

from musicape.items import MusicapeItem


class A51apeSpider(scrapy.Spider):
    '''爬取51ape中对应歌手的全部曲目'''
    name = '51ape'
    allowed_domains = ['51ape.com']
    start_urls = ['http://www.51ape.com/artist/']
    # http://www.51ape.com/skin/ape/php/qx_2.php?qx=()

    def parse(self, response):
        '''解析所有歌手页面'''

        # 歌手列表
        singer_list = response.xpath('//div[@class="gs_a"]/a/text()').extract()
        # 歌手链接列表
        singer_link_list = response.xpath('//div[@class="gs_a"]/a/@href').extract()
        # 遍历歌手链接列表
        for singer_link in singer_link_list:
            singer = singer_list[singer_link_list.index(singer_link)]
            # 判断是否是正常链接
            if 'javascript:void(0)' == singer_link:
                # 拼接链接
                singer_link = 'http://www.51ape.com/skin/ape/php/qx_2.php?qx=' + singer
                # 提交请求
            yield scrapy.Request(singer_link, callback=self.parse_song)
            # else:
            #     # 提交请求
            #     yield scrapy.Request(singer_link, callback=self.parse_singer)

    # def parse_song(self, response):
    #     '''解析歌曲对应的详情链接'''
    #     # 歌曲详情页链接列表
    #     song_link_list = response.xpath('//div[@class="w260 wd m mt_1 over"]/li/a/@href').extract()
    #     # 判断是否为空
    #     if len(song_link_list):
    #         # 遍历歌曲详情页列表
    #         for song_link in song_link_list:
    #             # 提交请求
    #              yield scrapy.Request(song_link, callback=self.parse_full)

    def parse_song(self, response):
        '''解析部分歌手多首歌曲的详情链接'''

        song_link_list = response.xpath('//div[@class="news w310 over fl"]/ul/li/a/@href|//div[@class="w260 wd m mt_1 over"]/li/a/@href').extract()
        if len(song_link_list):
            for song_link in song_link_list:
                yield scrapy.Request(song_link, callback=self.parse_full)
        # 翻页
        next_url = 'http://www.51ape.com' + response.xpath('//div[@class="mt_1 listpage b_t_d b_b_d lh50"]/a[last()-1]/@href').extract_first()
        # 下一页
        next_page = response.xpath('//div[@class="mt_1 listpage b_t_d b_b_d lh50"]/a[last()-1]/text()').extract_first()
        # 剔除空链接和不是下一页
        if next_url and next_page == '下一页':
            yield scrapy.Request(next_url, callback=self.parse_song)


    def parse_full(self, response):
        '''解析歌曲下载链接'''
        # 建立item对象
        item = MusicapeItem()
        # 获取数据
        # 歌手名  龙飘飘 - 梦中的娃娃.ape
        item['singer'] = response.xpath('//div[@class="fl over w638"]/h1/text()').extract_first().split(' - ')[0]
        # 歌曲名
        item['sname'] = response.xpath('//div[@class="fl over w638"]/h1/text()').extract_first().split(' - ')[1]
        # 歌曲专辑
        detail_list = response.xpath('//div[@class="fl over w638"]/h3/text()').extract()
        try:
            item['salbum'] = re.findall(r'选自专辑《(.*)》', detail_list[0])[0]
        except:
            item['salbum'] = None
        # 歌曲大小
        item['ssize'] = detail_list[2]
        # 歌曲语言
        item['slanguage'] = detail_list[3]
        # 歌曲发布时间
        item['stime'] = detail_list[4]
        # 歌曲下载链接
        item['down_link'] = response.xpath('//div[@class="fl over w638"]/a/@href').extract_first()
        # 歌曲下载密码
        down_pwd = response.xpath('//div[@class="fl over w638"]/b/text()').extract()[1]
        try:
            item['down_pwd'] = re.findall(r'密码：(.*)', down_pwd)[0]
        except:
            item['down_pwd'] = None

        yield item








