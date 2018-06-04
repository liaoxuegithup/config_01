#目的是跳转到新闻详情页
from . import news_blue
from flask import  request,current_app,jsonify,abort,session,render_template,abort,g
from info.models import News,User,tb_user_collection,Comment,CommentLike

from info import response_code,constants,db
from info.utils.comment import user_login


@news_blue.route("/comment_lickcount",methods=["POST"])
# 有点赞的情况，获取评论的id和新闻id
# 确定请求方式。post请求，接受参数
@user_login
def comment_lickcount():
#     首先判断用户是否存在，基于评论的，评论已经判断完毕，这里可判断，可不判断
    user = g.user
    print(user)
    if not user:
        return jsonify(erron=response_code.RET.DBERR, errsmg="用户未登录")
#     接受参数comment_id和news_id
    comment_id=request.json.get("comment_id")
    news_id = request.json.get("news_id")
    action= request.json.get("action")
# 在钱端一定是bool值用来判断，点赞还是取消点赞
#     判断参数是否存在
    if not all([comment_id,news_id,action]):
        return jsonify(erron=response_code.RET.PARAMERR, errsmg="缺少参数")
    # 查看数据库中lick_count是否存在,存在表示点赞,不存在表示没有点赞,取出和评论相关联的对象,在点出来
    comment=[]
    try:
        comment = Comment.query.filter(Comment.id == comment_id, Comment.news_id == news_id).all()
    except Exception as e:
        abort(405)
    # 将评论从数据库中取出来,然后判断评论是否存在(因为很可能不存在)
    if not comment:
        return jsonify(errno=response_code.RET.NODATA, errmsg='评论不存在')


# comment.like_count:不能直接查询获取用户点过赞的额评论

    comment_like_count = CommentLike.query.filter(CommentLike.user_id==user.id,CommentLike.comment_id ==comment_id).first()
    # 查询是该用户的评论的对象

    if action == "add":
        if not comment_like_count:
    #     如果点赞的数量在数据库中不存在,没有人点在(也就是可以点赞)
    # 将数据添加到数据库还需要将数据库中的所有对应必须加入的字段放进去
            comment_like_count = CommentLike()
            comment_like_count.user_id = user.id
            comment_like_count.comment_id = comment_id
            db.session.add(comment_like_count)
            Comment.like_count += 1
        try:
           db.session.commit()
        except Exception as e:
           db.session.rollback()
           current_app.logger.error(e)
           return jsonify(errno=response_code.RET.DBERR, errmsg='操作失败')
       #    每次添加完数据以后都需要将点击量同步到数据库,添加到数据库后代表点赞成功,所以要天际数据库后统计数据
       # else:
       #     不能取消(不对数据库进行操作)     e
    #     如果数据库中存在,1\不能在点了
    else:
        if comment_like_count:
           db.session.delete(comment_like_count)
           Comment.like_count -= 1
           try:
               db.session.commit()
           except Exception as e:
               db.session.rollback()
               current_app.logger.error(e)
               return jsonify(errno=response_code.RET.DBERR, errmsg='操作失败')

    return jsonify(errno=response_code.RET.OK, errmsg='操作成功')
#         如果不是添加,查看数据库中是否存在点赞,存在就取消,不存在添加



@news_blue.route("/news_comment",methods=["POST"])
@user_login
def news_comment():
#     首先判断用户存在，才可以评论
    user = g.user
    if not user:
        return jsonify(erron=response_code.RET.DBERR,errsmg="用户未登录")
#     form表但提交是post请求，用后台传递数据通过form
#     获取前端传过来的数据
    news_id = request.json.get("news_id")
#     获取评论信息

    comment_context = request.json.get("comment")
    parent_id = request.json.get("parent_id")
    if not all([news_id,comment_context]):
        return jsonify(erron = response_code.RET.PARAMERR,errsmg="缺少参数")
#     如果新闻存在
# 将新闻放入评论的数据库中
#     获取新闻数据
    news_id =int(news_id)



    try:
        news = News.query.filter(News.id==news_id).all()
        print(news)

        # print(comment.content)
        # 将获取的评论信息放入Comment的和use_id相同的表里面，是个列表
    #     谁评论的就将用户和评论信息加入到数据库
    # 列表对象没有append，还可以采用赋值的方式放入数据库
    # 当前用户当前评论
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=response_code.RET.DBERR, errmsg='操作失败')
    if not news:
        return jsonify(errno=response_code.RET.DBERR, errmsg='新闻不存在')

    comment = Comment()


    comment.user_id = user.id
    comment.news_id = news_id
    comment.content = comment_context
    # parent_id = int(parent_id)
    #         数据库中少了一个点赞条数
    if parent_id :
        comment.parent_id = parent_id


    print(comment)
    # 当前评论完毕，
    # 回复评论
    # 如果有父parent——id表示是回复评论
    # 后台需要将comment新增数据传过去
    # 将从前台获取的数据放入数据库

    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=response_code.RET.DBERR, errmsg='评论失败')

    return jsonify(errno=response_code.RET.OK, errmsg='操作成功',data=comment.to_dict())
    #    首先确定回复评论就是在页面中多了一个用户和用户的评论。在数据库中用户和父用户是多多多的关系，如果有ｐａｒｅｎｔ存在就代表是回父，如果不存在就是
    # 评论
@news_blue.route("/news_collect",methods=["POST"])
# 收藏新闻id,需要前端给我传过来新闻id和d
# iffuse收藏
# 之所以将收藏和取消收藏在写一个函数定义,是因为需要和 用户关联的数据库中存入数据,所以修改数据库需要用到post请求
# 所以用ajax,news_id,action
#
@user_login
def news_collect():
    # user_id=session.get("user_id")
    # nick_name=session.get("nick_name")
    user = g.user
    if not all([user]) :
        return jsonify(erron=response_code.RET.SESSIONERR ,errmsg="用户未登录")

    news_id = request.json.get("news_id")

    action= request.json.get("action")

    if not all([news_id, action]):
        # 虽然写上了取消ｉｄ和取消参数，参数限定的了自己执行自己的
        return jsonify(erron=response_code.RET.PARAMERR, ermasg="缺少参数")
#     在用户存在的情况下,从数据库中取出来和浏览器给我发过来的新闻id,,并将数据加入和数据库相关的库中
#     antion值必须是cancel_collect',collect
#     所以ａｎｔｉｏｎ必须在cancel_collect',collect，其它的不行
# 在数据库搜索 以后,将数据展现在模板上面
    if action not in ['cancel_collect','collect']:
        return jsonify(erron=response_code.RET.PARAMERR, ermasg="参数错误")
    if action =='collect':
        news= []

        # user = []
        try:
            news = News.query.get(news_id)


            # user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
            abort(405)

        if news not in  user.collection_news:


            user.collection_news.append(news)

        else:

            user.collection_news.remove(news)  #     每次只能添加一次数据
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)


            return jsonify(errno=response_code.RET.DBERR, errmsg='操作失败')




    return jsonify(errno=response_code.RET.OK, errmsg='操作成功')


#         收藏写完以后,写取消收藏
# 因为都是post的请求,接受参数,可以将两者放在一个路由里面
# 第一步获取取消以及取消新闻id的参数
# 判断参数是否存在,
# 判断用户是否存在
# 用户和收藏是否存在,
# 如果存在可以取消收藏
# 如何取消收藏，就是用户点击的新闻id,将ｉｄ从数据库中删除
# 理解因为news_id只是个接受用户收藏和取消的容器，两者可以通过ajax异步执行，增加新闻id3和取消id5
# （不知道对不对）




# 只有用户是登录的状态才可以有收藏的功能

# @news_blue.route("/detail/<int:news_id>",methods=["GET"])
@news_blue.route("/detail",methods=["GET"])
# def detail(news_id):
@user_login
def detail():
    # 根据前台需要,需要导入用户名,判断是get请求查寻数据直接将数据return就可以
    news_id=request.args.get("news.id:")

    user = g.user
    print(user)
    # if not user:
    #     return jsonify(errno=response_code.RET.SESSIONERR, errmsg='用户未登录')
    # 这里不应该,判断用户不存在,因为不关用户存不存在,就需要显示当前的页面(不等录的也应该可以看见)
    news=[]
    news_comments_count=[]
    try:
        news = News.query.filter(News.id ==news_id).first()


    except Exception as e:
        print(news)
        current_app.logger.error(e)
        # 判断数据库中的新闻是否存在,系统原因,报505,注意点news是对象需要将其变成字典
        # 当前页面只有一条数据,所以不需要遍历

    news_clicks = []
    # user=[]
    try:
        news_clicks = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
        # user = User.query.filter(User.id==user_id).first()
        print(user)
    except Exception as e:
        current_app.logger.error(e)
        #    威慑么是这样写,不应该是显示的是当前页的数据的点击量码?威慑么还是按着新闻点击量来()

    if not all([news,news_clicks]):
        abort(505)
    # 如果新闻存在,将数据发送到html中
    # 最初时的状态新闻的点击是0
    # 新闻点击量是 News.clicks,每运行一次,该新闻点击一次

    news.clicks +=1
    # 将累计的点击量放入数据库中
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)

    is_collected=False
    # if user_id:

    comment = []
    if user:
        if news in user.collection_news:
            is_collected = True
    #首先评论的内容显示在detail的页面里面，的内容
    # 从数据库中抽取数据，数据库是comment表
    try:
        comment = Comment.query.filter(Comment.news_id==news_id).order_by(Comment.create_time.desc()).all()
    # order_by(Comment.create_time.desc()).all()为什么按时间排序呢?
    # 因为获取出来的评论不是只有1条,用户评论过的数据全部都要显示在页面上面,并且按时间顺序排列
    # 这里不能使用get了,get只能取来对应的对象,不是集合
    # 评论的数据在用户存在的时候可以展示,在用户不存在的时候页要显示
    except Exception as e:
        current_app.logger.error(e)

    # 在detail.html页面需要将评论信息,从数据库拿出来,并发送给html以及点赞的数量
    # 点赞和取消点赞还需要定地来嗯个布尔值,传递给html
    # 展示出评论中的点赞数量(点赞或者没有点赞是根据bool值来判断
    # 将所有用户的点赞都取出来
    comment_line=[]
    if user:
        try:
            comment_like = CommentLike.query.filter(CommentLike.user_id ==user.id ).all()
            # 接下来将页面上排序的评论和用户点赞一一对应起来
            # 取出来所有被用户点赞的评论id
            comment_line = [ CommentLike.comment_id for comment_value in comment_like]
        except Exception as e:
            print(news)
            current_app.logger.error(e)
    # 点过赞的用户都取出来了,点郭赞的评论取出来了
    # 将所有的评论的id都取出来看看评论是否在用户点赞的评论id
    # is_like = False
    # if [user, comment.context]:
    #
    #     if comment.id in comment_line:
    #     #     评论的id在用户点过赞的id里面,就显示高亮,判断高亮的是is_like
    #         is_like=True
    # # 赞存在的前提是用户和评论都存在
    # else:
    #
    #     is_like = False
    # 为了方便使用model中的字典数据,将所有对象集合遍历出来,转化成字典的形式,最后将所有的字典放在打列表中转化成列表字典
    comment_list_dict=[]
    for comment in comment:
        comment_dict = comment.to_dict()
        comment_dict['is_like'] = False
        if comment.id in comment_line:
            comment_dict['is_like'] = True
        comment_list_dict.append(comment_dict)

    context={
        "user_id":user,

        "news":news.to_dict(),
        "news_clicks":news_clicks,
        'is_collected': is_collected,
        "comment":comment_list_dict,

    }

    # 从页面上
    # 从页面上可知需要动态传入点击量,detail.html据库中取出来
    return render_template("news/detail.html",context=context)


