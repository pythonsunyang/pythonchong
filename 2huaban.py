import requests
from bs4 import BeautifulSoup
import threading
from queue import Queue
import random,re
from urllib import request
from lxml import etree
numder_n = 3
class Start(threading.Thread):
    # 用代理访问
    proxy_list = [
         'http://61.155.104.111:3128',
        ]
    prxy_ip = random.choice(proxy_list)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
        }
    def __init__(self,bsea_url):
        super(Start,self).__init__()
        self.bsea_url = bsea_url
        self.img_list = []

    def run(self):
        self.info()

    # 处理函数 页面
    def getPage(self):
        # 随机抽取一个代理 进行访问
        list_url = []
        resopense = requests.get(url=self.bsea_url,headers=self.headers)
        html = BeautifulSoup(resopense.text,'lxml')
        # 获取地址  pin_id
        com = re.compile(r'"pin_id":(\d+?), "user_id"')
        res = com.findall(str(html))
        for page_ye  in res:
            info = 'http://huaban.com/pins/' + page_ye
            list_url.append(info) # 每一页  添加到列表等待request
        return list_url  #67
        # 提起图片 详情 内容
    def info(self):
        url_list  = self.getPage()
        print(url_list)
        for url in url_list:
            response =  requests.get(url,headers=self.headers)
            response.encoding = response.apparent_encoding
            com = re.compile(r'"orig_source":"(.*?)"')

            res = com.findall(response.text)
            print(res)
            self.img_list += res # 所有图片追加到一个列表
        print('——————————', self.img_list)
        # 重复 图片
        temp_list = []
        for one in self.img_list:
            if one not in temp_list:
                temp_list.append(one)
        print(temp_list)
        for img_info in temp_list:
            print(len(temp_list))
            img_name = img_info.split('/')[-1]
            print(img_name)
            request.urlretrieve(img_info,img_name + '.jpg')
            print('下载图片:',img_info)
if __name__ == '__main__':
    # q = Queue()
    # list_q = []
    bsea_url = 'http://huaban.com/favorite/beauty'
    # 测试--------------------------------------------------
    t = Start(bsea_url)
    t.start()
    # -----------------------------------------------------------
    # for i in range(numder_n):
    #     t = Start(bsea_url)
    #     list_q.append(t)
    # print(list_q)
    # t.start()
