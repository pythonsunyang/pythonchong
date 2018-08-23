
import requests
import pymysql
import random
from queue import Queue
import threading

db = pymysql.connect('192.168.71.132', 'root', '123456', 'ip66', charset='utf8')
cursor = db.cursor()

def all_mysql_ip():
    print(2)
    sql = 'select * from ip'
    cursor.execute(sql)
    results = cursor.fetchall()
    # 得出全部 代理信息  遍历每一条 put 队列
    for item in results:
        q_all_ip.put(item)  # 获取 数据库所有ip 数量 添加到队列
    db.commit()
    return q_all_ip   # 输出队列

class Proxy_my(threading.Thread):
    def __init__(self,q_all_ip):
        super(Proxy_my,self).__init__()
        self.q_all_ip = q_all_ip
    def run(self):
        # 下一步 删选ip



        proxy = self.rd()
        requests.get()
    def rd(self):
        ip = self.q_all_ip.get() # 提取ip 进行拼接
        proxy = {
            'http': 'http://' + ip[1] + ":" + str(ip[2]),
            'https': 'http://' + ip[1] + ":" + str(ip[2])
        }
        return  proxy

if __name__ == '__main__':

    q_all_ip = Queue()
    all_mysql_ip()
    print('提取出的ip个数',q_all_ip.qsize())
    # 调函数 把 所有ip 添加到队列
    start_list = []
    for i in range(3):
        t = Proxy_my(q_all_ip)
        t.start()
        start_list.append(t)
    for t in start_list:
        t.join()


