from flask import Flask    #导入Flask类
from flask_cors import CORS

app = Flask(__name__)         #实例化并命名为app实例
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__=="__main__":
    app.run(host="127.0.0.1", debug=True)   #调用run方法，设定端口号，启动服务