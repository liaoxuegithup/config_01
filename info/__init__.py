from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config_environment_app
import logging
from logging.handlers import RotatingFileHandler
def setup_log(level):
    """根据创建app时的配置环境，加载日志等级"""
    # 设置日志的记录等级
    logging.basicConfig(level=level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
# logs文件夹需要提交,但是log文件不需要提交,错误信息不需要别人知道
# 在push时git规定不能传空的文件夹,git规定在文件夹内创建.gitkeep文件


db = SQLAlchemy()
def fenzhang(config_name):
    app = Flask(__name__)
    app.config.from_object(config_environment_app[config_name])
    db.init_app(config_environment_app[config_name])

    # 以后都是以类的方式封装，方便修改和管理
    # 迁移管理和app相关联
    str = StrictRedis(host = config_environment_app[config_name].REDIS_HOST,post = config_environment_app["pro"].REDIS_POST)
    # 将redis的地址和端口号放到app的配置文件中
    # 那个环境下需要需要配置不同的redis,链接不同redis数据库,但是是否组要在不同环境下更改redis的ip吗
    # 开启CSRF保护
    CSRFProtect(app)
# 需要生成密钥
    return app
# 问题是db怎样传过去
# 解决办法是,在底层SQLAlchemy类直接调用init方法,将app以传参的方式,init直接调用app,可以给SQLAlchemy创建对象,用对象调用init方法来调用app
# 来解决每个环境都需要开启数据库的方式,那么为什么,manager里面不需要传,拥有环境配置信息的SQLAlchemy呢?(因为app传过去是给manager里面配置app的配置信息)
#------------------------------------------------------------------------
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from redis import StrictRedis
# from flask_wtf.csrf import CSRFProtect
# from flask_session import Session
# # from config import Config, DevlopmentConfig, ProductionConfig, UnittestConfig
# from config import configs
# import logging
# from logging.handlers import RotatingFileHandler
#
#
# def setup_log(level):
#     """根据创建app时的配置环境，加载日志等级"""
#     # 设置日志的记录等级
#     logging.basicConfig(level=level)  # 调试debug级
#     # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
#     file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
#     # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
#     formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
#     # 为刚创建的日志记录器设置日志记录格式
#     file_log_handler.setFormatter(formatter)
#     # 为全局的日志工具对象（flask app使用的）添加日志记录器
#     logging.getLogger().addHandler(file_log_handler)
#
#
# # 创建SQLAlchemy对象
# db = SQLAlchemy()
#
#
# def create_app(config_name):
#     """创建app的工厂方法
#     参数：根据参数选择不同的配置类
#     """
#
#     # 根据创建app时的配置环境，加载日志等级
#     setup_log(configs[config_name].LEVEL_LOG)
#
#     app = Flask(__name__)
#
#     # 获取配置信息
#     app.config.from_object(configs[config_name])
#
#     # 创建连接到MySQL数据库的对象
#     # db = SQLAlchemy(app)
#     db.init_app(app)
#
#     # 创建连接到redis数据库的对象
#     redis_store = StrictRedis(host=configs[config_name].REDIS_HOST, port=configs[config_name].REDIS_PORT)
#
#     # 开启CSRF保护：因为项目中的表单不再使用FlaskForm来实现，所以不会自动的开启CSRF保护，需要自己开启
#     CSRFProtect(app)
#
#     # 指定session数据存储在后端的位置
#     Session(app)
#
#     return app