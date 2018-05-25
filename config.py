# from redis import StrictRedis
# from unittest import TestCase
# import logging
# class Config(object):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/config_01"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = "fkdfkd"
#     REDIS_HOST = "127.0.0.1"
#     REDIS_POST = 6379
#     SESSION_TYPE = "redis"
# #   设置SESSION设置在redis库中
#     SESSION_REDIS = StrictRedis(host= REDIS_HOST)
# #     指定Session存储到后端的位置c,
#     SESSION_USE_SIGNR = True
# #     开启31天
#     PERMANENT_SESSION_LIFETIME = 60*60*24
# # 定义醒目的生产环境,保证项目在哪个环境下都不出错,生产环境有3个
# # 开发环境(写代码),生产环境(准备上线,将所有代码链接在一起),测试环境(在上线之前检查代码是否有问题)
# # 需要定义三个环境的目的是不同环境在整个项目中配置不同,基于config
# # 在每个开发环境下都需要用日志记录信息,很容易的观察哪里是否有错误
# class Develop(Config):
#     # 开发环境基本基于config
#     LOG_LEVE = logging.DEBUG
#     pass
#
# class Production(Config):
#     # 生产环境将所有代码封装的过程,不需要测试
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/config_pro_01"
#     LOG_LEVE = logging.DEBUG
# class TestEnvironment(TestCase):
#     # 测试环境TestCase里面封装了debug
#     LOG_LEVE = logging.DEBUG
#     SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/config_test_01"
#     # 修改父类的配置信息后,还需要保证在运行的时候app.config里面的配置信息在改变,即运行生产环境就放生产环境的,开发就放开发的配置信息
#     # 所以在init里面app的参数是变动的,可以以传参的方式向app里面传变量因为是向app中传不同的参数,app不能动,所以需要将app封装起来
#     # 可以使用basconvert字典的形式,将类名传过去info那边可以根据以建取值类名的方式,执行方法,basconvert里封装了类名可以调用对应的属性
# config_environment_app = {
#     'dev':Develop,
#     'pro' :Production,
#     'test':TestEnvironment,
# }
# -------------------------------------------------------
from redis import StrictRedis
import logging


class Config(object):
    """配置文件的加载"""

    # 项目秘钥：CSRF/session,还有其他的一些签名算法会用
    SECRET_KEY = 'q7pBNcWPgmF6BqB6b5VICF7z7pI+90o0O4CaJsFGjzRsYiya9SEgUDytXvzFsIaR'

    # 开启调试模式
    DEBUG = True

    # 配置MySQL数据库连接信息:真实开发中，要使用mysql数据库的真实IP
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/information_29'
    # 不去追踪数据库的修改，节省开销
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置redis数据库:因为redis模块不是flask的扩展，所以就不会自动的从config中读取配置信息，只能自己读取
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # 指定session使用什么来存储
    SESSION_TYPE = 'redis'
    # 指定session数据存储在后端的位置
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 是否使用secret_key签名你的sessin
    SESSION_USE_SIGNER = True
    # 设置过期时间，要求'SESSION_PERMANENT', True。而默认就是31天
    PERMANENT_SESSION_LIFETIME = 60*60*24 # 一天有效期


# 以下代码是封装不同开发环境下的配置信息

class DevlopmentConfig(Config):
    """开发环境"""
    # 开发环境和父类基本一致

    # 开发环境日志等级
    LEVEL_LOG = logging.DEBUG


class ProductionConfig(Config):
    """生产环境"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/information_pro_29'
    # 生产环境日志等级
    LEVEL_LOG = logging.ERROR


class UnittestConfig(Config):
    """测试环境"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/information_case_29'
    # 生产环境日志等级
    LEVEL_LOG = logging.DEBUG


# 定义字典，存储关键字对应的不同的配置类的类名
configs = {
    'dev':DevlopmentConfig,
    'pro':ProductionConfig,
    'unit':UnittestConfig
}