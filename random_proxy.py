
import requests
import pymysql
import random
from queue import Queue
import threading

class RandomProxy():
# 获取 数据库所有ip 数量 添加到队列
    def __init__(self):
        self.q_all_ip = Queue()
        self.one_all_ip = Queue()
        self.db = pymysql.connect('192.168.71.132', 'root', '123456', 'ip66', charset='utf8')
        self.cursor = self.db.cursor()
    # 提取 数据库 所有 ip 信息
    def all_mysql_ip(self):
        sql = 'select * from ip'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        # 得出全部 代理信息  遍历每一条 put 队列
        for item in results:
            self.q_all_ip.put(item)
        self.db.commit()
        return self.q_all_ip   # 输出队列
    def proxy(self): # 随机 获取 中一条 ip
        q_all_ip = self.all_mysql_ip()
        print(q_all_ip.qsize())
        for item in q_all_ip.get():
            print(item)
        # print(self.one_all_ip.qsize())

if __name__ == '__main__':

    # 调函数 把 所有ip 添加到队列
    t = RandomProxy().proxy()
    # t.start()

