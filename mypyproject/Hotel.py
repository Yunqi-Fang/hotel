from flask import jsonify
from pymysql import connect
from pymysql.cursors import DictCursor
from sqlalchemy import null

from settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE



class Hotel(object):
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

    def get_hotel_info(self, hotelid):
        sql = 'select * from hotel WHERE hotelid = %s'
        val = (hotelid)
        self.cursor.execute(sql, val)
        hotelinfo = self.cursor.fetchone()
        return hotelinfo

    def change_hotel_info(self, hotelid, hoteldict):
        sql = ("UPDATE hotel SET address = %s, hotelName = %s, inoroutTime = %s, foreignGuest = %s, introduction = %s, "
               "phone = %s, score = %s, type = %s WHERE hotelid = %s")
        val = (
            hoteldict['address'],
            hoteldict['hotelName'],
            hoteldict['inoroutTime'],
            hoteldict['foreignGuest'],
            hoteldict['introduction'],
            hoteldict['phone'],
            hoteldict['score'],
            hoteldict['type'],
            hotelid
        )
        self.cursor.execute(sql, val)
        self.conn.commit()
        if self.cursor.rowcount > 0:
            return True
        else:
            return False

    def add_hotel(self, hotel):
        hotelName = hotel["hotelName"]
        type = hotel["type"]
        score = hotel["score"]
        phone = hotel["phone"]
        address = hotel["address"]
        introduction = hotel["introduction"]
        foreignGuest = hotel["foreignGuest"]
        inoroutTime = hotel["inoroutTime"]


        sql = f"INSERT INTO hotel (hotelName, type, score, phone, address, introduction, foreignGuest, inoroutTime) VALUES ('{hotelName}', '{type}', {score}, '{phone}', '{address}', '{introduction}', '{foreignGuest}', '{inoroutTime}');"
        self.cursor.execute(sql)
        self.conn.commit()
        if self.cursor.rowcount > 0:
            return True
        else:
            return False