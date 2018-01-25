# http://oldhouse.hfhouse.com/sale/
import re
import threading
from queue import Queue
import requests, json
import time
from lxml import etree


class Zhongxin(object):
    """
    中信信托信托信息爬虫CITIC Trust
    """
    def __init__(self):
        self.url_list = [
            "https://trust.ecitic.com/CPZQ/index.jsp?columnid=92&columnName=房地产信托",
            "https://trust.ecitic.com/CPZQ/index.jsp?columnid=93&columnName=矿产能源信托",
            "https://trust.ecitic.com/CPZQ/index.jsp?columnid=94&columnName=金融机构信托",
            "https://trust.ecitic.com/CPZQ/index.jsp?columnid=95&columnName=工商企业信托",
            "https://trust.ecitic.com/CPZQ/index.jsp?columnid=96&columnName=基础设施信托",
        ]
        self.file = open("./file/" + "xintuo.json", "w")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }
        # 构建一个存放请求url的队列
        self.url_queue = Queue()
        # 构建一个存放列表页信息的队列
        self.detail_data_queue = Queue()
        # 构建一个存放保存的信息的队列
        self.save_data_queue = Queue()

    def __del__(self):
        self.file.close()

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        # with open("text_cont", "wb") as f:
        #     f.write(response.content)
        return response.content

    def get_detail_data(self):
        while True:
            url_list = self.url_queue.get()
            for url in url_list:
                response = requests.get(url, headers=self.headers)
                self.detail_data_queue.put(response.content)
            self.url_queue.task_done()

    def get_detail_url_list(self, data):
        # print(len(data))
        # 创建element对象
        html = etree.HTML(data)
        # re匹配出帖子节点列表

        node_list = re.findall(r'<a href="(/product/.*?.shtml)" target="_blank">.*?</a>', data.decode())
        # print(node_list)

        detail_url_list = []

        for node in node_list:
            detail_url = "https://trust.ecitic.com/" + node
            # print(detail_url)

            detail_url_list.append(detail_url)
        try:
            next_url = "https://trust.ecitic.com/CPZQ/" + \
                       html.xpath('//*[@id="cRight"]/div/div[4]/div[3]/div[1]/a[last()]/@href')[0]
        except:
            next_url = None

        # print(detail_url_list, next_url)

        # return detail_url_list, next_url
        self.url_queue.put(detail_url_list)
        return next_url

    def parse_data(self):
        while True:
            data = self.detail_data_queue.get()
            print("开始处理数据")
            """
            <td width="411">(.*?)</span></td>.*?<td><span>(.*?)
    </span></td>.*?<td><span>(.*?)
    </span></td>.*?<td><span>(.*?)
    </span></td>.*?<tr class="odd">
            """
            node_list = re.findall(
                r'<td width="411"><span>(.*?)</span></td>.*?<td><span>(.*?)\r\n</span></td>.*?<td><span>(.*?)\r\n</span></td>.*?<td><span>(.*?)\r\n</span></td>.*?<tr class="odd">',
                data.decode(), re.S)

            data_list = []
            # 遍历节点列表，从没一个节点中抽取数据
            for data in node_list:
                temp = dict()

                temp['title'] = data[0]
                temp['scale'] = data[1]
                temp['shouyi'] = re.sub(r"\r\n", "", data[2])
                temp['time'] = data[3]

                # print(temp)
                data_list.append(temp)
            # print(data_list)
            # return data_list
            self.save_data_queue.put(data_list)
            self.detail_data_queue.task_done()

    def save_data(self):
        while True:
            data_list = self.save_data_queue.get()
            # print(data_list)
            for data in data_list:
                # print(dir(data))
                # str_data = data.str() + ',\n'
                str_data = json.dumps(data, ensure_ascii=False) + ',\n'
                self.file.write(str_data)
            self.save_data_queue.task_done()

    def get_url(self):
        for next_url in self.url_list:
            while True:
                data = self.get_data(next_url)
                next_url = self.get_detail_url_list(data)
                if next_url is None:
                    break

    def run(self):
        # # 构建url
        # for url in self.url_list:
        #     next_url = url
        #     # print(next_url)
        #     # 翻页
        #     while True:
        #         # 获取数据
        #         data = self.get_data(next_url)
        #         # 处理数据
        #         next_url = self.get_detail_url_list(data)
        #         for detail_url in detail_url_list:
        #             detail_data = self.get_detail_data()
        #             data_list = self.parse_data()
        #             # 保存数据
        #             self.save_data()
        #         if next_url is None:
        #             break
        # 创建一个存放线程任务的列表
        thread_task_list = list()

        t_0 = threading.Thread(target=self.get_url)
        thread_task_list.append(t_0)

        for i in range(10):
            t_1 = threading.Thread(target=self.get_detail_data)
            thread_task_list.append(t_1)

        for i in range(10):
            t_2 = threading.Thread(target=self.parse_data)
            thread_task_list.append(t_2)

        for i in range(10):
            t_3 = threading.Thread(target=self.save_data)
            thread_task_list.append(t_3)

        for t in thread_task_list:
            # 守护线程
            t.setDaemon(True)
            # 开始线程
            t.start()

        time.sleep(3)

        # 设置主线程等待所有的队列为空后再结束
        self.url_queue.join()
        self.detail_data_queue.join()
        self.save_data_queue.join()


if __name__ == '__main__':
    zhongxin = Zhongxin()
    zhongxin.run()
