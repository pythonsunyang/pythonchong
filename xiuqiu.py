from urllib import request
import requests
import json
import pymysql

class Xqiu(object):
    def __init__(self,url):
        self.base_url = url
        self.headers = {
                "Accept": "*/*",
                # "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Cookie": "device_id=cb58c8df1862e00e0c6be317df3ebc6b; _ga=GA1.2.1440478559.1531271921; __utmz=1.1531271944.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); s=el11jj8uvi; bid=875ebf8d37089af8ba8a9f2acc1477cf_jjgjqxff; __utma=1.1440478559.1531271921.1531275893.1531278609.3; aliyungf_tc=AQAAAN1rsw4q6gcAUhVFeYMj91oKJUeR; xq_a_token=584d0cf8d5a5a9809761f2244d8d272bac729ed4; xq_a_token.sig=x0gT9jm6qnwd-ddLu66T3A8KiVA; xq_r_token=98f278457fc4e1e5eb0846e36a7296e642b8138a; xq_r_token.sig=2Uxv_DgYTcCjz7qx4j570JpNHIs; _gid=GA1.2.2024838083.1534295992; _gat_gtag_UA_16079156_4=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1534295992; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1534295992; u=491534295992868",
                "Host": "xueqiu.com",
                "Referer": "https://xueqiu.com/",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
        }
    def page(self):
        response = requests.get(self.base_url,headers=self.headers)
        response.encoding = response.apparent_encoding
        data = response.text
        data = json.loads(data)
        # 获得 每一页 的最后一条id
        id_list = []
        data_info_list = []
        info = data['list']
        for i in info:  # 获取详情 每一条的数据
             id = i['id']
             data_info = i['data']
             id_list.append(id)
             data_info_list.append(data_info)
        # 存储文件 data 到mysql数据库
        # print(data_info_list)

        for u in data_info_list:
            u = json.loads(u)
            info_id = u['id']
            info_name = u['title']
            info_description = u['description']
            info_target = u['target']
            info_target = 'https://xueqiu.com' + info_target  # 新闻详情地址
            sql = "INSERT INTO xueqiu(ip,sname,description,target) values('%s','%s','%s','%s')" % (info_id,info_name,info_description,info_target)
            print(info_id)
            my_sql.mysql_sql(sql)  # 存储 mysql
        last_id = str(id_list[-1])
        return last_id # 下一个json 页数
class my_sql(object):
    def __init__(self):
        # 192.168.71.132','root','123456','img_pic',charset='utf8'
        self.connect = pymysql.connect('127.0.0.1','root','123456','py10',charset='utf8')
        self.cursor = self.connect.cursor()
    def mysql_sql(self,sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except:
            self.connect.rollback()
    def __del__(self):
        self.connect.close()
        self.cursor.close()

if __name__ == '__main__':
    i = -1  # 定义一个标识变量  为第一页
    my_sql = my_sql()  # 实例化 mysql
    for j in range(3):
        base_url = 'https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id={}&count=15&category=101'.format(i)
        X = Xqiu(base_url)
        i=X.page() # 页数
