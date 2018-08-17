#  封装
from urllib import request,parse
from urllib.request import HTTPError,URLError

def get(url,headers=None):
    return urlresponse(url=url,headers=headers)

def post(url,headers=None,data=None):
    return urlresponse(url=url, headers=headers,data=data)

def urlresponse(url,headers=None,data=None):  # data 传入的必须是字典
    if  not headers:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
    try:
        if data: # 为真是 post
            data = parse.urlencode(data)
            data_bytes = data.encode('utf-8')
            res = request.Request(url=url,headers=headers,data=data_bytes)
        else:  #为假是 get
            res = request.Request(url=url, headers=headers,)
        response = request.urlopen(res)
        html = response.read().decode('utf-8')
        return html
    except HTTPError as e :
        print('系统超时')
    except URLError as e :
        print('404错误')

if __name__ == '__main__':
    url = 'http://www.baidu.com/'
    print(get(url,))
    print(post(url,data={'kw':'你好'}))