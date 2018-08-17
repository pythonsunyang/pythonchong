#  百度翻译
from urllib import request,parse
import json
def Go(kw,headers=None,): # post
    url = 'http://fanyi.baidu.com/sug'
    if not headers:
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
    data = {
        "kw": kw
    }
    try:
        data = parse.urlencode(data)
        data_bytes =  data.encode('utf-8')
        print(data_bytes)
        res = request.Request(url,headers=headers,data=data_bytes)
        response = request.urlopen(res)
        res_dict = json.loads(response.read().decode('utf-8'))
        return res_dict['data'][0]['v']
    except IndexError as e:
        print('输入格式错误')


if __name__ == '__main__':
    data = input('请输入汉字：')
    print(Go(data))