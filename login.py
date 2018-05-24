from flask import Flask
# 给项目立项，立项是以manage运行
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
# 立项以后给项目增加配置文件
# 然后集成mysql数据库和redis数据库
# 两者性能不同，mysql性能比较差，redis一般放在内存和磁盘
# 因为redis不是flask中的扩展工具，要使用app的配置文件需要将redis和app建立练习
# 设置CRST保护
# 设置Session
# Session可以保存到redis数据库,mysql数据库,还有文件,这里选择存储到redis
#
# Session的密钥可以在Session里面是用/CSRF用
class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/config_01"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "fkdfkd"

    HOST = "127.0.0.1"
    POST = 6379
# 给app添加配置文件

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
# 以后都是以类的方式封装，方便修改和管理
# 迁移管理和app相关联
manager  = Manager(app)
# 将app和数据库和脚本命令相关联
Migrate(app,db)
# 将脚本命令当中的MigrateCommand放入管理器
manager.add_command("db",MigrateCommand)



str = StrictRedis(host = Config.HOST,port=Config.POST)
# 将redis的地址和端口号放到app的配置文件中
# 开启CSRF保护
CSRFProtect(app)
# 需要生成密钥



@app.route('/index')
def index():
    return "index page"



if __name__ == '__main__':
    manager.run()