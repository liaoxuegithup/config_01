from flask import Flask
# 给项目立项
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
# 立项以后给项目增加配置文件
# 然后集成mysql数据库和redis数据库
# 两者性能不同，mysql性能比较差，redis一般放在内存和磁盘
# 因为redis不是flask中的扩展工具，要使用app的配置文件需要将redis和app建立练习

class Config(object):
    DEBUG = True

# 给app添加配置文件

app = Flask(__name__)
app.config.from_object(Config)
# 以后都是以类的方式封装，方便修改和管理


db = SQLAlchemy(app)

str = StrictRedis(host = "192.168.68.139",port=6379)
# 将redis的地址和端口号放到app的配置文件中

@app.route('/index')
def index():
    return "index page"



if __name__ == '__main__':
    app.run()