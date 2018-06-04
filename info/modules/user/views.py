#用户中心必须是要在用那户登录的状态
from . import user_blue
from flask import g,jsonify,render_template,redirect,url_for,request,current_app,session
from info.utils.comment import user_login
from info.utils.image_storage import storage

# from flask import  request,current_app,jsonify,abort,session,render_template,abort,g
from info.models import db
#
from info import response_code
#
@user_blue.route("/user_pic",methods=["GET","POST"])
@user_login

def user_pic():
#     点击图片时是get请求,返回的是user_pic表单
    user = g.user
    if not user:
        return redirect(url_for("user/user_center"))
        #     首先点击基本信息,会向浏览器发送请求,返回一个表格
    if request.method == "GET":
        context = {
            'user': user,
        }
        return render_template('news/user_pic_info.html', context=context)
    if request.method =="POST":
        avatar = request.files.get("avatar")
#        图片可以用files直接获取表单里面图片的值
        if not avatar:
#             如果图片不存在,应该给个默认头像
           avatar =
#         如果存在,将图片上传到七牛云
        avatar_qiniu = sorted(avatar)
#     上传后将图片路径存入到数据库中



# 基本信息页
@user_blue.route("/user_infomation",methods=["GET","POST"])
@user_login
def user_infomation():
#     判断用户是否存在
     user = g.user
     if not user:
         return redirect(url_for("user/user_center"))
#     首先点击基本信息,会向浏览器发送请求,返回一个表格
     if request.method=="GET":
         context = {
             'user': user,
         }
         return render_template('news/user_base_info.html', context=context)
#      接下来是post请求,接受用户上传的基本信息
     if request.method =="POST":
#          接受参数signature,nick_name,gender
        signature= request.json.get("signature")

        nick_name=request.json.get("nick_name")

        gender=request.json.get("gender")
#         判断数据是否存
        if not all([ signature,nick_name,gender]):
            return jsonify(errno=response_code.RET.DBERR, errmsg="缺少参数")
#         如果参数存在,将数据存入数据库,并将数据发送给前端,渲染出来,还应该放在redis中一份,做状态保持

        user.signature =  signature
        user.nick_name = nick_name
        user.gender = gender
        try:

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return jsonify(errno=response_code.RET.DBERR, errmsg="操作失败")
        # 当用户点击保存以后,应该跳转到显示修改后的信息的页面

        session["nick_name"]=nick_name

     # return redirect(url_for('user.user_center'))
     return jsonify(errno=response_code.RET.OK, errmsg='修改基本资料成功')





@user_blue.route("/user_center")
@user_login
def user_center():
    # 首先判断用户是否存在
    # 判断请求方式是get请求
    # 如果用户存在返回user.html页面
    # 效果是当点击名字或者头像时跳转到我命名的路径上面
    user = g.user
    if not user:
        return redirect(url_for('index.index'))
    context={
        'user':user,
    }
    return render_template("news/user.html",context=context)

