from redis import StrictRedis
class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/config_01"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "fkdfkd"
    REDIS_HOST = "127.0.0.1"
    REDIS_POST = 6379
    SESSION_TYPE = "redis"
#   设置SESSION设置在redis库中
    SESSION_REDIS = StrictRedis(host= REDIS_HOST)
#     指定Session存储到后端的位置c,
    SESSION_USE_SIGNR = True
#     开启31天
    PERMANENT_SESSION_LIFETIME = 60*60*24
