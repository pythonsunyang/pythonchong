import requests


def get_proxy():
    url = 'http://dps.kdlapi.com/api/getdps/?orderid=903559094569781&num=1&pt=1&dedup=1&sep=1'
    response = requests.get(url)
    return response.text

if __name__ == '__main__':
    proxy = get_proxy()
    print(proxy)