from redis import StrictRedis
from unittest import TestCase
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
# 定义醒目的生产环境,保证项目在哪个环境下都不出错,生产环境有3个
# 开发环境(写代码),生产环境(准备上线,将所有代码链接在一起),测试环境(在上线之前检查代码是否有问题)
# 需要定义三个环境的目的是不同环境在整个项目中配置不同,基于config
class Develop(Config):
    # 开发环境基本基于config
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/config_01"
    pass

class Production(Config):
    # 生产环境将所有代码封装的过程,不需要测试
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/config_pro_01"

class TestEnvironment(TestCase):
    # 测试环境TestCase里面封装了debug
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/config_test_01"