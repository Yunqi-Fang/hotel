from pymysql import connect
from pymysql.cursors import DictCursor
from settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


class User(object):
    def __init__(self):
        self.conn = connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT,
            charset='utf8')
        self.cursor = self.conn.cursor(DictCursor)  # 返回字典形式

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def get_user_info(self):
        user_info_list = []
        sql = 'select * from user'
        self.cursor.execute(sql)
        for temp in self.cursor.fetchall():
            user_info_list.append(temp)
        return user_info_list
