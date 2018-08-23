import pymysql
class my_sql(object):
    def __init__(self):
        # 192.168.71.132','root','123456','img_pic',charset='utf8'
        self.db = pymysql.connect('127.0.0.1','root','123456','py10',charset='utf8')
        self.cursor = self.db.cursor()
    def mysql_sql(self,sql,data):
        try:
            #  sql = "INSERT INTO xueqiu(ip) values('%s',)" % (info_id)
            #  sql 语句 格式
            self.cursor.execute(sql,data)
            self.db.commit()
        except:
            self.db.rollback()
    def updata(self):
        pass
    def dal_sql(self):
        pass
    def __del__(self):
        self.db.close()
        self.cursor.close()
if __name__ == '__main__':
    my_sql = my_sql()
    sql ='insert into num(sname) VALUES (13)'
    my_sql.mysql_sql(sql)