from flask import jsonify
from pymysql import connect
from pymysql.cursors import DictCursor
from sqlalchemy import null

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

    def user_login(self, username):
        sql = "SELECT password, role, hotelid FROM user WHERE username = %s"
        val = (username)
        self.cursor.execute(sql, val)
        dbUser = self.cursor.fetchone()
        # 验证密码是否匹配
        if dbUser:
            return dbUser
        else:
            return null

    def user_register(self, username, password, role, hotelid):
        sql = "INSERT INTO user (username, password, role, hotelid) VALUES (%s, %s, %s, %s)"
        val = (username, password, role, hotelid)
        self.cursor.execute(sql, val)
        self.conn.commit()
        if self.cursor.rowcount > 0:
            return True
        else:
            return False
