# -*- coding: utf-8 -*-
import json
import re
import requests
import time
from lxml import etree
from selenium import webdriver


class Ape51(object):
    '''爬取51ape中对应歌手的全部曲目'''

    def __init__(self):
        # 构建url
        self.url = 'http://www.51ape.com/artist/'

        # 构建headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }

        # 创建浏览器对象
        self.dr = webdriver.Chrome()
        # self.dr = webdriver.PhantomJS()
        self.dr.maximize_window()

        # 定义存放数据列表
        self.singer_list = list()
        self.song_detail_list = list()
        self.song_down_list = list()

        # 定义保存数据文件
        self.song_file = open('song.json', 'w', encoding='UTF-8')
        self.detail_file = open('song_detail.json', 'w', encoding='UTF-8')

    def __del__(self):
        self.song_file.close()
        self.detail_file.close()

    def get_data(self, url):
        '''发送请求, 获取响应'''
        resp = requests.get(url, headers=self.headers)
        return resp.content

    def parse_singer_song(self):
        '''解析数据'''
        # 定位到所有歌手页面节点
        a_list = self.dr.find_elements_by_xpath('//div[@class="gs_a"]/a')

        # 获取数据
        # singer_list = list()

        for a in a_list:

            # 判断是否是页面小窗口
            # 如果有页面小窗口, 直接获取到歌曲详情页url
            if a.get_attribute('href') == 'javascript:void(0)':
                # 点击前给一个加载页面时间
                time.sleep(0.3)
                a.click()
                # 定位页面小窗口中的歌曲节点
                song_list = self.dr.find_elements_by_xpath('//div[@class="qx_php"]/div/li/a')
                # 判断列表长度, 长度不止一个进行遍历
                if len(song_list) > 1:
                    singer_song = dict()
                    singer_song['singer'] = a.text
                    sl_list = list()
                    for sl in song_list:
                        # 弹出页面小窗口歌手的歌曲链接
                        song_dict = dict()
                        song_dict['song_name'] = sl.text
                        song_dict['song_link'] = sl.get_attribute('href')
                        sl_list.append(song_dict)
                    # 将多个歌曲, 放入列表, 再以value值存入字典
                    singer_song['song'] = sl_list
                    print(singer_song)
                    self.song_detail_list.append(singer_song)
                else:
                    # 列表中只有一首歌曲
                    singer_song = dict()
                    singer_song['singer'] = a.text
                    song_dict = dict()
                    singer_song['song'] = song_dict
                    try:
                    	song_dict['song_name'] = song_list[0].text
                    except:
                    	song_dict['song_name'] = None
                    try:
                    	song_dict['song_link'] = song_list[0].get_attribute('href')
                    except:
                    	song_dict['song_link'] = None
                    print(singer_song)
                    self.song_detail_list.append(singer_song)
                # 延时, 给一个存储时间
                time.sleep(0.2)
                self.dr.find_element_by_xpath('//div[contains(@class, "close")]').click()

            # 否则是一个歌手的全部曲目的链接, 此时是会刷新新的页面
            else:
                singer_song = dict()
                singer_song['singer'] = a.text
                singer_song['song'] = a.get_attribute('href')
                print(singer_song)
                print('=' * 50)
                self.singer_list.append(singer_song)

    def parse_some_singer(self):
        '''抽取部分歌手的歌曲信息'''
        # 遍历部分歌手列表
        for singer in self.singer_list:
            # 定义用来存储多个歌曲信息列表
            list_song = list()
            singer_dict = dict()
            singer_dict['singer'] = singer['singer']
            # 可能有多页, 需要循环
            while singer['song']:
                # 发送请求, 获取响应
                data = self.get_data(singer['song'])
                # 建立element对象
                html = etree.HTML(data)
                # //div[@class="news w310 over fl"]/ul/li  歌曲节点
                # //div[@class="mt_1 listpage b_t_d b_b_d lh50"]/a[last()-1]  下一页
                # 获取歌曲列表
                el_song = html.xpath('//div[@class="news w310 over fl"]/ul/li')
                for el_s in el_song:
                    # 歌曲信息字典
                    el_dict = dict()
                    el_dict['song_link'] = el_s.xpath('./a/@href')[0]  # 歌曲链接
                    el_dict['song_num'] = el_s.xpath('./span[1]/text()')[0]  # 歌曲编号
                    list_song.append(el_dict)
                # 获取下一页的元素对象
                next_page = html.xpath('//div[@class="mt_1 listpage b_t_d b_b_d lh50"]/a[last()-1]')
                # 判断是否有下一页,
                if not len(next_page):
                    break
                elif next_page[0].xpath('./text()')[0] == '下一页':
                    singer['song'] = 'http://www.51ape.com' + next_page[0].xpath('./@href')[0]
                else:
                    # 此处虽然取到next_page值, 但是不是我们想要的, 所以结束循环
                    break
            # 多个歌曲以列表形式存入字典
            singer_dict['song'] = list_song
            print(singer_dict)
            print('-' * 50)
            self.song_detail_list.append(singer_dict)

    def parse_download_data(self):
        '''根据歌曲详情页获得歌曲下载url和提取密码, 还有详细信息'''
        '''
        {'singer': 'A Fine Frenzy', 'song': {'song_name': 'A Fine Frenzy - Almost Lover.ape', 'song_link': 'http://www.51ape.com/ape/13010.html'}}
        '''
        # 遍历歌曲列表
        for detail in self.song_detail_list:

            data = detail['song']

            # 判断数据类型
            if type(data) == type(dict()):
                detail_dict = dict()
                # 一个歌手, 一首歌曲
                # 发送请求, 获取详情页响应
                try:
                	detail_data = self.get_data(data['song_link'])
                except:
                	continue
                # 建立element对象
                html = etree.HTML(detail_data)
                # 获取数据
                detail_list = html.xpath('//div[@class="fl over w638"]/h3/text()')
                detail_dict['singer'] = detail['singer']  # 歌手名
                detail_dict['sname'] = html.xpath('//div[@class="fl over w638"]/h1/text()')[0]  # 歌曲名
                # detail_dict['salbum'] = detail_list[0]  # 专辑名
                try:
                	detail_dict['salbum'] = re.findall(r'选自专辑《(.*)》', detail_list[0])[0]  # 专辑名
                except:
                	detail_dict['salbum'] = None
                detail_dict['ssize'] = detail_list[2]  # 歌曲大小
                detail_dict['slanguage'] = detail_list[3]  # 歌曲语言
                detail_dict['stime'] = detail_list[4]  # 歌曲更新时间
                detail_dict['down_link'] = html.xpath('//div[@class="fl over w638"]/a/@href')[0]  # 歌曲百度下载链接
                # detail_dict['down_pwd'] = html.xpath('//div[@class="fl over w638"]/b/text()')[1]
                # 密码提取时, 需要注意源码中是换行后, 取出来有两个, 取下标为1的值, 然后再用正则匹配出密码
                # 匹配密码时, 冒号是中文的冒号
                # 有可能没有密码, 所以try一下
                try:
                    detail_dict['down_pwd'] = \
                    re.findall(r'密码：(.*)', html.xpath('//div[@class="fl over w638"]/b/text()')[1])[0]
                except:
                    detail_dict['down_pwd'] = None
                print(detail_dict)

                print('+' * 50)
                self.song_down_list.append(detail_dict)

            else:
                # print(data)
                # num = 0
                # 一个歌手, 多首歌曲
                detail_dict = dict()
                # 定义存放多个歌曲列表
                song_detail_list = list()
                detail_dict['singer'] = detail['singer']  # 歌手名
                for data_dict in data:
                    # 每次循环是一个歌曲的信息
                    one_song = dict()
                    # 发送请求, 获取详情页响应
                    # print(data_dict['song_link'])
                    try:
                    	detail_data = self.get_data(data_dict['song_link'])
                    except:
                    	continue
                    # 建立element对象
                    html = etree.HTML(detail_data)
                    # 获取数据
                    detail_list = html.xpath('//div[@class="fl over w638"]/h3/text()')

                    one_song['sname'] = html.xpath('//div[@class="fl over w638"]/h1/text()')[0]  # 歌曲名
                    # detail_dict['salbum'] = detail_list[0]  # 专辑名
                    try:
                        # print(detail_list[0])
                        one_song['salbum'] = re.findall(r'选自专辑《(.*)》', detail_list[0])[0]  # 专辑名
                    except:
                        one_song['salbum'] = None
                    one_song['ssize'] = detail_list[2]  # 歌曲大小
                    one_song['slanguage'] = detail_list[3]  # 歌曲语言
                    one_song['stime'] = detail_list[4]  # 歌曲更新时间
                    one_song['down_link'] = html.xpath('//div[@class="fl over w638"]/a/@href')[0]  # 歌曲百度下载链接
                    # detail_dict['down_pwd'] = html.xpath('//div[@class="fl over w638"]/b/text()')[1]
                    # 密码提取时, 需要注意源码中是换行后, 取出来有两个, 取下标为1的值, 然后再用正则匹配出密码
                    # 匹配密码时, 冒号是中文的冒号
                    # 有可能没有密码, 所以try一下
                    try:
                        one_song['down_pwd'] = \
                            re.findall(r'密码：(.*)', html.xpath('//div[@class="fl over w638"]/b/text()')[1])[0]
                    except:
                        one_song['down_pwd'] = None
                    print(one_song)
                    print('+' * 50)
                    # num += 1
                    # print(num)
                    # 将单首歌曲存入列表
                    song_detail_list.append(one_song)
                detail_dict['song'] = song_detail_list
                self.song_down_list.append(detail_dict)

    def save_song_data(self):
        '''保存歌手和歌曲数据'''
        self.song_file.write('{"Desc": "save singer and song detail url"},\n\n')
        for detail in self.song_detail_list:
            detail_str = json.dumps(detail, ensure_ascii=False) + ',\n'
            self.song_file.write(detail_str)

    def save_detail_data(self):
        '''保存歌曲详细信息数据'''
        self.detail_file.write('{"Desc": "save singer, sname, salbum, ssize, stime, sdown_link, sdown_pwd"},\n\n')
        for down in self.song_down_list:
            down_str = json.dumps(down, ensure_ascii=False) + ',\n'
            self.detail_file.write(down_str)

    def run(self):
        '''程序运行开始'''
        # 发送请求
        self.dr.get(self.url)
        # 页面延时
        self.dr.implicitly_wait(10)
        # 解析歌手页面获取的数据
        self.parse_singer_song()
        # 解析部分歌手歌曲数据(因为部分歌手歌曲较多, 会更新出新的页面, 需要另外处理)
        self.parse_some_singer()
        # 保存歌手和歌曲详情页链接
        self.save_song_data()
        # 解析歌曲下载链接
        self.parse_download_data()        
        # 保存歌曲下载链接和密码
        self.save_detail_data()


if __name__ == '__main__':
    ape51 = Ape51()
    ape51.run()
