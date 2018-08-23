#  时间的天数的 运算
import datetime
from datetime import timedelta

def day(num):
    '''
    :param num: 要减去时间的天数
    :return:
    : a  当前的日期
    '''
    b = timedelta(days=num)
    a = datetime.datetime.now()
    return (a - b).strftime('%Y-%m-%d')
if __name__ == '__main__':
    pass