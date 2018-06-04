from . import index_blue
from flask import  render_template,current_app,session,request,jsonify
from info.models import News,User,Category
from info import response_code,constants
#从新定义函数
@index_blue.route("/news_list")
def index_new():
    #     1\首先确认请求方式是get请求
    #     2\用户需要将新闻的种类,看第几页,以及一页有多少行发过来
    # 1\获取参数,如果取出来不是整数不能让程序崩溃

    cid = request.args.get("cid",1)
    # 接受用户的要查看的新闻种类,默认是更新的新闻(在js里面显示了)
    page = request.args.get("page",1)
    #用户看的第几页,默认看的是1页
    # 使用get方法后面参数是1,取出来的值也是1

    per_page = request.args.get("per_page",10)
    print(per_page)
    try:
        cid = int(cid)
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)


        return jsonify(errno=response_code.RET.PARAMERR, errmsg='参数错误')
    # 一页有多少条数据
# 为什么这里不需要判断这些数据是否存在呢
# 新闻分为两种情况,默认是更新页,按着时间倒序的方式 排列,并且取出来多少页数据,如果没有页数就不取值
# 第二种情况按着种类时间倒序的方式排列
# 注意点news存放的是列表对象,jsonfily只认识,列表,字典列表,字典,需要将其转化,转化之前需要将每个对象取出来
    paginate=[]
    if cid ==1:
        try:
            paginate = News.query.order_by(News.create_time.desc()).paginate(page, per_page, False)
        #     per_page指的是10条信息
        except Exception as e:
            current_app.logger.erron(e)
    else:
        try:
            paginate = News.query.filter(News.category_id==cid).order_by(News.create_time.desc()).paginate(page, per_page, False)
        except Exception as e:
            current_app.logger.erron(e)
    news = paginate.items
# 取出当前页所有模型对象
# 尖括号代表对象,里面的数字代表数据在内存中存的数据


    page = paginate.pages
    # 读取分页的总页数
    total_page = paginate.per_page
    # 读取当前是第几压
    # 将对象转成json认识的列表字典
    news_dict_list=[]
    for new in news:
        news_dict_list.append(new.to_basic_dict())
#     将数据发送给浏览器
#     获取6个id数据,将前端页面变成动态的


    data={
        "news_dict_list":news_dict_list,
        "page":page,
        "total_page":total_page
    }
#     给前端发送数据
    return jsonify(errno=response_code.RET.OK, errmsg='OK', data=data)

@index_blue.route('/')
def index():
    # 打开主页如果登录会显示登录和退出
    #  如果没有登录会显示登录和注册
    # 在打开主页显示点击排行,(就是将html中死的值改变成动态的)
    # 排行的特点
    # 1\将所有的新闻按着时间倒序的方式排列
    # 步骤:当用户请求的页面的时候,数据应该随着主页面发送过去,请求方式是
    # get请求,数据从数据库中取出来
    # 发送的位置在点击排行
    # 思路先看session里面是否有值
    user_id = session.get('user_id',None)
    user_nick_name = session.get("nick_name",None)
    user = None
    if  user_id:
        # 如果用户存在,会显示登录和注册,就是将用户名法给前端,必须从数据库中取值,因为session只能存在30分钟

        try:
            user = User.query.get(user_id)
        #     这个user_id指的是数据库中的字段码

        except Exception as e:
            current_app.logger.eron(e)
    # 会显示登录和推出
    # print(user)
    news = []
    try:
       news = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    #    所有的新闻根据点击排行排列,news是对象,直接发过去浏览器不认识,limit是啥意思了
    #    print(news)
    except Exception as e:
       current_app.logger.erron(e)
    category=[]
    try:
        category = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)

    context = {
        'user' : user,
        "news_clicks" :news,
        "category":category
    }
    return render_template('news/dase.html', context = context)

@index_blue.route("/favicon.ico")
def favcion():
    return current_app.send_static_file("news/favicon.ico")
# 返回的 是可以找到图片的路径,curent_app是全局使用的
# send_static_file里面封装了当调用时会返回静态路径加参数路径
