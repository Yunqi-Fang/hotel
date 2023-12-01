from flask import jsonify
from pymysql import connect
from pymysql.cursors import DictCursor
from sqlalchemy import null

from settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE



class Room(object):
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

    def change_room_info(self, hotelid, roomid, roomdict):
        sql = ("UPDATE room SET roomType = %s, roomPrice = %s, roomcount = %s, number = %s WHERE hotelid = %s and "
               "roomid = %s")
        val = (
            roomdict['roomType'],
            roomdict['roomPrice'],
            roomdict['roomcount'],
            roomdict['number'],
            hotelid,
            roomid
        )
        self.cursor.execute(sql, val)
        self.conn.commit()
        if self.cursor.rowcount > 0:
            return True
        else:
            return False

    def add_room(self, room):
        hotelId = room["hotelId"]
        roomType = room["roomType"]
        roomPrice = room["roomPrice"]
        roomcount = room["roomcount"]
        number = room["number"]

        sql = f"INSERT INTO room (hotelId, roomType, roomPrice, roomcount, number) VALUES ('{hotelId}', '{roomType}', {roomPrice}, '{roomcount}', '{number}');"
        self.cursor.execute(sql)
        self.conn.commit()
        if self.cursor.rowcount > 0:
            return True
        else:
            return False