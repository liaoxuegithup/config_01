from info import fenzhang,db
# 给项目立项，立项是以manage运行
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from config import config_environment_app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session

# 立项以后给项目增加配置文件
# 然后集成mysql数据库和redis数据库
# 两者性能不同，mysql性能比较差，redis一般放在内存和磁盘
# 因为redis不是flask中的扩展工具，要使用app的配置文件需要将redis和app建立练习
# 设置CRST保护
# 设置Session
# Session可以保存到redis数据库,mysql数据库,还有文件,这里选择存储到redis
#flask中有可扩展的FLak_Session,可将session存储到redis
# Session的密钥可以在Session里面是用/CSRF用
# 在Session底层是可以通过配置文件中config[key]取值
# class Config(object):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/config_01"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = "fkdfkd"
#     REDIS_HOST = "127.0.0.1"
#     REDIS_POST = 6379
#     SESSION_TYPE = "redis"
# #   设置SESSION设置在redis库中
#     SESSION_REDIS = StrictRedis(host= REDIS_HOST,post =  REDIS_HOST)
# #     指定Session存储到后端的位置c
#     SESSION_USE_SIGNR = True
# #     开启31天
#     PERMANENT_SESSION_LIFETIME = 60*60*24
#     设置时间


# 给app添加配置文件

# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
# # 以后都是以类的方式封装，方便修改和管理
# # 迁移管理和app相关联
# str = StrictRedis(host = Config.HOST,port=Config.POST)
# # 将redis的地址和端口号放到app的配置文件中
# # 开启CSRF保护
# CSRFProtect(app)
# # 需要生成密钥
app = config_environment_app["pro"]
# 在项目运行入口只需要每个环境的配置信息,在项目入口需要启动信息,所以这边不需要,环境和启动信息相关联的配置信息
manager  = Manager(app)
# 将app和数据库和脚本命令相关联
Migrate(app,db)
# 将脚本命令当中的MigrateCommand放入管理器
manager.add_command("db",MigrateCommand)







@app.route('/')
def index():
    return "index page"



if __name__ == '__main__':
    manager.run()