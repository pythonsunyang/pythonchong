#  封装
from urllib import request,parse
from urllib.request import HTTPError,URLError
from http.cookiejar import CookieJar
import json
class session(object):
    #  用类 __init__ 方法 把 cookiejar 存储到
    def __init__(self):
        cookoe_object = CookieJar()
        handler = request.HTTPCookieProcessor(cookoe_object)
        self.opener = request.build_opener(handler)

    def get(self,url,headers=None):
        #  get 请求 调用 下面的 get函数   都需要传输 opener  因为不知道 是否需要 CookieJar
        #   所有要把 CookieJar 的 值 传入
        return get(url,headers=headers,opener=self.opener)

    def post(self,url,headers=None,data=None):
        # post 需要传入 data    传入值一定 要是字典类型
        return post(url,headers=headers,data=data,opener=self.opener)
# --------------------------------------------------------------------------------------------------------------------

def get(url,headers=None,opener=None):
    return urlresponse(url=url,headers=headers,opener=opener)

def post(url,headers=None,data=None,opener=None):
    return urlresponse(url=url, headers=headers,data=data,opener=opener)

def urlresponse(url,headers=None,data=None,opener =None):  # data 传入的必须是字典
    if  not headers:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
    html = b''
    try:
        if data: # 为真是 post
            data = parse.urlencode(data)
            data_bytes = data.encode('utf-8')
            req = request.Request(url=url,headers=headers,data=data_bytes)
        else:  #为假是 get
            req = request.Request(url=url, headers=headers,)
        if opener:
            response = opener.open(req)
        else:
            response = request.urlopen(req)
        html = response.read().decode('utf-8')
    except HTTPError as e :
        print('系统超时')
    except URLError as e :
        print('404错误')
    return html

if __name__ == '__main__':
    url = 'https://www.cnblogs.com/horanly/p/6604104.html'
    s = session()
    print(s.get(url))
    # s = session()
    # url = 'http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=201872151079'
    # data = {
    #     "email": "14704649955",
    #     "icode": "",
    #     "origURL": "http://www.renren.com/home",
    #     "domain": "renren.com",
    #     "key_id": "1",
    #     "captcha_type": "web_login",
    #     "password": "66bcf3f298f6ad6b00656ae474bea7fd99ccf874aaced0b30016a6485e98c875",
    #     "rkey": "43ba526df574399dc99674bddcc083ad",
    #     "f": "http%3A%2F%2Fzhibo.renren.com%2Ftop"
    # }
    # post_ = s.post(url,data=data)
    # post_ = json.loads(post_)
    # print(post_)
    # print(s.get(post_['homeUrl']))
