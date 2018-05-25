from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
# 以后都是以类的方式封装，方便修改和管理
# 迁移管理和app相关联
str = StrictRedis(host = Config.HOST,port=Config.POST)
# 将redis的地址和端口号放到app的配置文件中
# 开启CSRF保护
CSRFProtect(app)
# 需要生成密钥