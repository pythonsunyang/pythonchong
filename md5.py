import hashlib
# 封装 md5 加密
def md5(data):
        md_5 = hashlib.md5()
        md_5.update(str(data).encode(encoding='utf-8'))
        return md_5.hexdigest()
if __name__ == '__main__':
    pass