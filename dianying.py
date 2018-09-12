import requests
import threading
from queue import Queue
import re
import time
import pymysql
import json

count = 10   # 线程数量
page =  3   # 爬去页数
class Theading(threading.Thread):
    def __init__(self,q_data_list,q_take_list,f):
        super(Theading,self).__init__()
        self.q_data_list = q_data_list # 传入的数据队列(空)
        self.q_take_list = q_take_list # 存储输入 给解析函数
        self.f = f
    def run(self):
        self.getPage()
        # if self.q_take_list.
        self.analysis()
    def getPage(self):  #  每页页面数据
        full_url = self.q_data_list.get()
        # print(full_url)
        response = requests.get(full_url)
        response.encoding = response.apparent_encoding
        html = response.text
        list_url = re.findall(r'<a href="(.*?)" class="ulink">.*?</a>',html)
        for i in list_url:
            # print(i)
            full_url = 'http://www.dytt8.net' +  i
            # 拼接 URL 地址 加入队列
            self.q_take_list.put(full_url)
        return self.q_take_list
    def analysis(self):  # 解析页面提取数据
        if self.q_take_list.qsize() == 0:
            return
        else:
            if not self.q_take_list.empty():
                data_dict = {}
                print(self.q_take_list.qsize())  # 每页的电影个数
                try:
                    for i in range(1,q_take_list.qsize()):
                        data_url = self.q_take_list.get()
                        # print(data_url)
                        response = requests.get(data_url)
                        response.encoding = response.apparent_encoding
                        html = response.text
                        # 连接
                        data_href = re.findall(r'<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(.*?)">',html)
                        data_str = data_href[0]   #  连接 下载地址
                        print(data_str)
                        pat = re.compile(r'com\.(.*?)\.') # 死侍2未分级加长版.BD.720p.中英双字幕
                        res = pat.search(data_str)
                        data_name = res.group(1)     # 名字
                        data_dict['电影名字'] = data_name
                        data_dict['电影下载地址'] = data_str
                        all_dianying = json.dumps(data_dict,ensure_ascii=False,indent=4)
                        print(all_dianying)
                        print(data_name, '名字')
                        self.f.write(all_dianying+ ',')
                        time.sleep(0)
                except:
                    self.analysis()
# class my_sql
# //*[@id="pl_unlogin_home_leftnav"]/div/ul/div[2]/li/a


if __name__ == '__main__':
    f = open('dianying1.json','w' ,encoding='utf-8')
    url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_%d.html'
    q_data_list = Queue()
    q_take_list = Queue()
    for i in range(1,page):  # 爬所有页数 添加到队列
        full_url = url % i
        q_data_list.put(full_url)
    pege_start_list = []
    for i in range(1,count): # 采集   把队列 传入类  进行提取
        t = Theading(q_data_list,q_take_list,f)
        t.start()
        pege_start_list.append(t)
    for t in pege_start_list:
        t.join()

