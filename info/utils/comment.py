#自定义过滤器
from flask import session,current_app,g
from info.models import User
from functools import wraps
def do_rank(index):
    if index ==1:
        return 'first'
    elif index ==2:
        return  'second'
    elif index ==3:
        return 'third'
    else:
        return ""
# def user_login(view_func):
#     # view_func接受的是个函数名
#     def wrapper(*args,**kwargs):
#     #     具体获取登录用户信息的逻辑
#          user_id = session.get("user_id",None)
#          # 判断用户是否存在
#          if user_id:
#          #     表是用户已经存在
#             try:
#                 user = User.query.get(user_id)
#             except Exception as e:
#                 current_app.logger.error(e)
#
#         # 使用全局的g变量存储查询出来的登录用户信息
#          g.user = user

        # 执行被装饰的视图函数
    #      return view_func(*args, **kwargs)
    #
    # return wrapper
def user_login(func):
    @wraps(func)
    def wapper(*args,**kwargs):
        #　着里面可以复用最外面函数的参数，如果给函数传参可以放在ｗａｐｐｅｒ函数里面
        user=None
        try:
            user_id = session.get("user_id",None)
            # 在这里用户信息判断过了
            # user_nick_name = session.get("nick_name")
            if user_id:
                user = User.query.get(user_id)
        # get的使用方法是获取ｕｓｅｒ_id的对象，而ｆｉｒｓｔ是获取符合条件的列表（存对象），对吸纳给使用None，列表使用[]
        except Exception as e:
            current_app.logger.error(e)

        g.user = user
        print(g.user)
        return func(*args,**kwargs)
    return  wapper
# 这里是定义一一种方法，ｆｕｎｃ只是接受函数的引用，传哪个函数，是由装饰在哪里，哪里使用这个方法。


