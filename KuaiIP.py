#  下载   存储   测试ip 是否可用
import requests
from lxml import etree
import multiprocessing
from multiprocessing import Pool,Queue
import re
import json,time
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}

def download_ip(li_list):  # 下载 IP存储
    for full_url in li_list:
        print('下载ip地址',full_url)
        response = requests.get(full_url,headers = headers)
        html = response.text
        html = etree.HTML(html)
        # 提取 ip 地址
        data_all_ip = html.xpath('//div[@id="list"]/table/tbody/tr')
        for ip in data_all_ip:
            ip_storage = {}
            ip_info = ip.xpath('./td/text()')[0]
            post_info = ip.xpath('./td/text()')[1]
            ip_storage['ip'] = ip_info
            ip_storage['port'] = post_info
            ip_storage = json.dumps(ip_storage, ensure_ascii=False, indent=4)
            with open('kuaiIP_ALL.json', 'a') as f:
                f.write(ip_storage)
def info_page(full_url,q_queue): # 提取ip  # q_queue 传进为空
    print('IP加入队列函数',q_queue.qsize())
    global headers
    response = requests.get(full_url,headers = headers)
    html = response.text
    html = etree.HTML(html)
    # 提取 ip 地址
    data_all_ip = html.xpath('//div[@id="list"]/table/tbody/tr')
    for ip in data_all_ip:
        ip_info = ip.xpath('./td/text()')[0]
        post_info = ip.xpath('./td/text()')[1]
        q_queue.put((ip_info,post_info))
    # q_queue.put(res)
def Verification(info_ip,):  # 解析ip函数
    print(info_ip)
    proxy = {
        'http': 'http://' + info_ip[0] + ":" + str(info_ip[1]),
        'https': 'http://' + info_ip[0] + ":" + str(info_ip[1])
    }
    print('使用代理ip',proxy)
    # 设置代理ip
    url = 'https://www.baidu.com/s?wd=ip'
    response = requests.get(url=url,proxies=proxy,timeout = 5)
    # 返回状态码
    if 200 <= response.status_code <= 300:
        print('可以使用的ip地址',info_ip,response.status_code)
        ip_storage = {}
        ip_storage['ip'] = info_ip[0]
        ip_storage['port'] = info_ip[1]
        print(info_ip)
        ip_storage = json.dumps(ip_storage,ensure_ascii=False,indent=4)
        with open('kuaiIP.json', 'a') as f:
            f.write(ip_storage+',')
    else:
        print('不可以使用的ip地址', info_ip, response.status_code)
if __name__ == '__main__':
    q_queue = Queue()
    #  定义个列表存储 每一页的ip 地址
    ip_list = []
    for i in range(1,101):
        base_url = 'https://www.kuaidaili.com/free/intr/%s/'
        full_url =  base_url % i
        print(full_url)
        ip_list.append(full_url)
        p = multiprocessing.Process(target=info_page, args=(full_url,q_queue,))
        p.start()
    #   下载IP  存储 为JSON  的进程
    download_ip_def = multiprocessing.Process(target=download_ip, args=(ip_list,))  #  传入 列表  所有的地址
    download_ip_def.start()
    time.sleep(5)

    q_qool = Pool(3)
    n = 0
    while 1:
        if not q_queue.empty():
            info_ip = q_queue.get()   # 提取队列每一个的IP
            print('提取IP队列剩余',q_queue.qsize())
            print('提取网页的IP地址',info_ip)
            q_qool.apply_async(Verification,(info_ip,))   # 传入 测试ip 函数
            n = 0
        else:
            n += 1
            time.sleep(3)
            if n ==10:
                break
            continue
    q_qool.close()
    q_qool.join()
    # 程序最后退出前进行join
    download_ip_def.join()





