from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import Config,config_environment_app
db = SQLAlchemy()
def fenzhang(config_environment_app):
    app = Flask(__name__)
    app.config.from_object(config_environment_app["pro"])
    db.init_app("bianglaing")

    # 以后都是以类的方式封装，方便修改和管理
    # 迁移管理和app相关联
    str = StrictRedis(host = config_environment_app["pro"].REDIS_HOST,post = config_environment_app["pro"].REDIS_POST)
    # 将redis的地址和端口号放到app的配置文件中
    # 那个环境下需要需要配置不同的redis,链接不同redis数据库,但是是否组要在不同环境下更改redis的ip吗
    # 开启CSRF保护
    CSRFProtect(app)
# 需要生成密钥
    return app
# 问题是db怎样传过去
# 解决办法是,在底层SQLAlchemy类直接调用init方法,将app以传参的方式,init直接调用app,可以给SQLAlchemy创建对象,用对象调用init方法来调用app
# 来解决每个环境都需要开启数据库的方式,那么为什么,manager里面不需要传,拥有环境配置信息的SQLAlchemy呢?(因为app传过去是给manager里面配置app的配置信息)
