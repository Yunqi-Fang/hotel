from flask import Flask, jsonify, request, make_response  # 导入Flask类
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null
from sqlalchemy.orm import sessionmaker

from Hotel import Hotel
from Room import Room
from User import User
from flask_bcrypt import Bcrypt

'''
返回接口如下：
{
    code: 200/500
    data: #数据位置，一般为数组
    message: '对本次请求的说明'
}
'''

app = Flask(__name__)  # 实例化并命名为app实例
CORS(app)

app.config['JSON_AS_ASCII'] = False

bcrypt = Bcrypt(app)


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    users = User()
    userList = users.get_user_info()
    res = {
        "code": 200,
        "data": userList,
        "messege": "获取到全部用户信息"
    }
    return jsonify(res)


@app.route("/login", methods=['POST', 'GET'])
def login():
    getJson = request.get_json()
    username = str(getJson.get('username'))  # json数据格式
    password = str(getJson.get('password'))  # json数据格式

    users = User()
    dbuser = users.user_login(username)
    # role = dbuser['role']
    # hotelid = duuser['hotelid']
    if dbuser != null and bcrypt.check_password_hash(dbuser['password'], password):
        # 若用户名和密码匹配，则返回登录成功的消息
        res = {
            "code": 200,
            "data": getJson,
            "messege": "登陆成功"
        }
    else:
        # 若用户名和密码不匹配，则返回登录失败的消息
        res = {
            "code": 500,
            "data": getJson,
            "messege": "登陆失败"
        }
    return make_response(res)


@app.route("/hotelinfo/<hotelid>", methods=['POST', 'GET'])
def hotelinfo(hotelid):
    hotel = Hotel()
    hotelInfo = hotel.get_hotel_info(hotelid)
    res = {
        "code": 200,
        "data": hotelInfo,
        "messege": f"查看酒店id为{hotelid}的酒店信息"
    }

    return make_response(res)


@app.route("/register", methods=['POST', 'GET'])
def register():
    # 注册逻辑
    getJson = request.get_json()
    username = str(getJson.get('username'))  # json数据格式
    password = str(getJson.get('password'))  # json数据格式
    role = str(getJson.get('role'))  # json数据格式
    hotelid = int(getJson.get('hotelid'))

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    users = User()

    # 检查
    if request.method == 'POST':
        ans = users.user_register(username, hashed_password, role, hotelid)
        if ans:
            res = {
                "code": 200,
                "data": dict(getJson),
                "messege": "注册成功"
            }
        else:
            res = {
                "code": 500,
                "data": dict(getJson),
                "messege": "注册失败"
            }
        return make_response(res)


# 新增酒店
@app.route("/hotel/add", methods=['POST'])
def add():
    hotel = Hotel()
    getJson = request.get_json()
    hoteldict = dict(getJson)
    print(hoteldict)
    hotelInfo = hotel.add_hotel(hoteldict)
    if hotelInfo:
        res = {
            "code": 200,
            "data": hotelInfo,
            "messege": "新增酒店成功"
        }
    else:
        res = {
            "code": 500,
            "data": hotelInfo,
            "messege": "新增酒店失败"
        }

    return make_response(res)




# 新增客房
@app.route("/room/add", methods=['POST'])
def add_room():
    room = Room()
    roomJson = request.get_json()
    roomdict = dict(roomJson)
    print(roomdict)
    roomInfo = room.add_room(roomdict)
    if roomInfo:
        res = {
            "code": 200,
            "data": roomInfo,
            "messege": "新增客房成功"
        }
    else:
        res = {
            "code": 500,
            "data": roomInfo,
            "messege": "新增客房失败"
        }

    return make_response(res)


@app.route("/changeroominfo/<hotelid>/<roomid>/<userhotelid>", methods=['PUT', 'GET'])
def changeroominfo(hotelid, roomid, userhotelid):
    if userhotelid == hotelid:
        room = Room()
        roomJson = request.get_json()
        roomdict = dict(roomJson)
        ans = room.change_room_info(hotelid, roomid, roomdict)
        if ans:
            res = {
                "code": 200,
                "data": ans,
                "messege": "修改客房信息成功"
            }
        else:
            res = {
                "code": 500,
                "data": ans,
                "messege": "修改客房信息失败,未进行改动"
        }
    else:
        res = {
            "code": 500,
            "data": '',
            "messege": "只能处理所属酒店的工作"
        }
    return make_response(res)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)  # 调用run方法，设定端口号，启动服务
