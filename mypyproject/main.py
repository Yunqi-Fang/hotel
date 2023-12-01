from flask import Flask, jsonify  # 导入Flask类
from flask_cors import CORS
from User import User

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


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    users = User()
    userList = users.get_user_info()
    return jsonify(userList)


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)  # 调用run方法，设定端口号，启动服务
