from . import passport_blue
from flask import request,abort,make_response,current_app,jsonify,session
from info import redis_store,constants,response_code,db
# 注意在导入redis_store中.它不是全局变量,导出来出错,所以需要在info下的init文件中定义全局变量
from info.utils.captcha.captcha import captcha
from info.libs.yuntongxun.sms import CCP
import json,re,random,datetime
from info.models import User
@passport_blue.route('/logout', methods=['GET'])
# 退出登录
# 就是将保持状态中的值删掉
def logout():
    try:
        session.pop("mobile",None)
#         为什么要有None
        session.pop("user_id",None)
        session.pop("nick_name",None)
        print(session)
    #     一个一个删除数据的原因,是因为csrf_token的值页存在session

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=response_code.RET.DBERR, errmsg='退出登录失败')
    return jsonify(errno = response_code.RET.OK,errmsg="退出成功")
@passport_blue.route('/login',methods = ["POST"])

# 注册用户
def login():
#     用户登录
# 获取客互输入的手机号和,密码,和数据中的数据进行比较
    json_dict = request.json
    mobile = json_dict.get('mobile')
    password = json_dict.get('password')
    if not all([mobile,password]):
        return jsonify(errno = response_code.RET.DBERR,errmsg="缺少参数")
    if not re.match(r'^1[345678][0-9]{9}$', mobile):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='手机号格式错误')
    try:
#         从数据库中将手机号和密码取出来,为了保证和取出来的值是这个用户的,可以采用过滤的方式,取出来是对象
       user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
       current_app.logger.error(e)
       return jsonify(errno=response_code.RET.DBERR, errmsg='查询用户数据失败')
    if not user:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='用户名或密码错误')

    if not user.check_password(password):
        # user.check_password(password可以直接
        return jsonify(errno=response_code.RET.PWDERR, errmsg='用户名或密码错误')

    # 如果想要完成一串动作,即注册即登录,或者登录后即跳转到首页,就需要使用session来做状态保持,因为session的有效期是30分钟
    # 而且注册就一次,平时都是登录,为了保障



    user.last_login = datetime.datetime.now()
    try:
        db.session.commit()
    #     提交是啥
    except Exception as e:
        current_app.logger.error(e)



        return jsonify(errno=response_code.RET.DBERR, errmsg='记录最后一次登录的时间失败')


    db.session.rollback()
    session['mobile'] = user.mobile
    session['user_id'] = user.id
    session['nick_name'] = user.nick_name

    # 为了保证平时用着方便所以将手机号,用户名,用户id村里面

    return jsonify(errno = response_code.RET.OK,errmsg='登录成功')
#   登录成功即显示登录信息


@passport_blue.route('/register',methods =["POST"] )
# 'mobile':mobile,
#             'smscode':smscode,
#             'password':password
#         };
#
#         $.ajax({
#             url:'/passport/register'
# 定义函数的目的是传入手机验证码,
# 原理:必须在校验验证码通过以后在进行获取手机验证码
def register():
# 因为手机号不能让别人看见,所以使用的是post请求方式
#     获取手机号,验证码和密码明问
    json_dict = request.json
#     获取用户输入
    mobile = json_dict.get('mobile')
    smscode = json_dict.get('smscode')
    # 获取用户输入的手机验证码,然后在生成验证码的额时候将验证码保存,两个共同点是值相同,从数据库当中通过"SMS"+mobile的建找到对应的值,然后进行对比
    password =json_dict.get('password')
#     判断这些数据是否存在
    if not all([mobile,smscode,password]):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='缺少参数')
# 如果存在判断,手机号的格式是否正确
    if not re.match(r'^1[345678][0-9]{9}$', mobile):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='手机号格式错误')
# 将smscode和在redis中的值进行比较
    smscode_mobile = redis_store.get("SMS"+mobile)
    if not smscode_mobile:
        return jsonify(errno=response_code.RET.NODATA, errmsg='短信验证码不存在')
    if smscode !=smscode_mobile:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='输入短信验证码有误')



    user = User()
    user.mobile = mobile
    user.nick_name = mobile
# 这是什么意思
    user.password = password
# user中没有password的属性
# 记录最后一次登录时间
    user.last_login = datetime.datetime.now()
    try:
        db.session.add(user)
        db.session.commit()
    #     一个用户名执行存储一次,也就保证了每个人的key是唯一的
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=response_code.RET.DBERR, errmsg='保存注册数据失败')
#     将手机号和密码存入session中,用于状态保持
# 之前校验失败手机号和用户名竟然存到了数据库里面
    session['user_id'] = user.id
    session["mobile"] = mobile
    session['nick_name'] = user.nick_name
    return jsonify(errno=response_code.RET.OK, errmsg='注册成功')

@passport_blue.route("/sms_code",methods = ["POST"])
# mobile':mobile,
#         'image_code':imageCode,
#         'image_code_id':imageCodeId
#     };
#
#     // TODO 发送短信验证码
#     $.ajax({
#         url:'/passport/sms_code',
def sms_code():
#     获取手机号
# 获取验证码
# 第一次不用存手机号
# 验证码对比失败,应该是验证码的值取的不对,检查获取的验证码是否正确,检查从server中获取的值是否正确
    json_dict = request.json
    mobile = json_dict.get("mobile")
    image_code_client  =json_dict.get("image_code")
    image_code_id= json_dict.get("image_code_id")
    print('id1-----------------------',image_code_id)
# 从客户端获取的验证码应该和从服务器获取的验证码一致,在前端在获取值的时候,会绑定uuid
# 校验参数是否存在
    if not all([mobile, image_code,image_code_client]):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='缺少参数')
# 判断手机格式是否正确
    if not re.match(r'^1[345678][0-9]{9}$', mobile):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='手机号格式错误')
# 校验手机验证码是否和redis中的匹配,在这之前先判断在服务器中是否存在这个验证码?,(不存在的原因是已经失效了)如果不存在就不用往下判断了
    try:
        image_code_id_server = redis_store.get('ImageCode:' + image_code_id)
        print('id------------------------',image_code_id_server)
    #     这是空的
    except Exception as e:
        current_app.logger(e)
        return jsonify(errno=response_code.RET.DBERR, errmsg='查询图片验证码失败')
        # 如果数据库中获取失败,给客户友好提示
    if not image_code_id_server:
        return jsonify(errno=response_code.RET.DBERR, errmsg='查询图片验证码失败')
    if image_code_client.lower()!= image_code_id_server.lower():
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='输入验证码有误')
# 如果存在,给手机号发送短信
    sms_code = '%06d'%random.randint(0,99999)
    result = CCP().send_template_sms(mobile, [sms_code, 5], 1)
    if result !=0:
    # if not result:
        return jsonify(errno=response_code.RET.THIRDERR, errmsg='发送短信验证码失败')
#     反之发送成功,成功后将手机号作为建,将手机验证码存储到redis中
    try:
        redis_store.set("SMS"+mobile,sms_code,constants.SMS_CODE_REDIS_EXPIRES)
#         将手机号以建的方式存储验证码
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=response_code.RET.DBERR, errmsg='保存短信验证码失败')

# 7.响应短信验证码发送的结果
    return jsonify(errno=response_code.RET.OK, errmsg='发送短信验证码成功')


# 使用荣联云发送短信,但是需要自己设定随机数

@passport_blue.route("/image_code",methods =[ "GET"])
# '/passport/image_code?imageCodeId='+imageCodeId;
# 钱端设定了点击图片事件
def image_code():
# 现在的目的是给前端传递图片验证码,功能是当点击图片局部刷新产生新的验证码,当页面整体刷新时产生新的验证码,为了验证传递的唯一性,通过uuid作为唯一标识
# 1 获取uuid
    imageCodeId = request.args.get("imageCodeId")
    print( imageCodeId)
     # 这里不太理解imageCodeId是前端给的值,必须用这个
  # 2 判断uuid是否存在
    if not imageCodeId:
        abort(403)
        # 如果uuid不存在的话,前端写错了
        # 如果存在,就生成验证码

    name,text,image= captcha.generate_captcha()
    current_app.logger.debug(text)
        # 生成验证码的工具会放在工具文件里面,name是啥,验证码即可以生成图片还可以生成数字
        # 将生成好的验证码和对应的uuid放在redis里面,存储的目的是,为了后续校验用,不是状态保持

    try:
        redis_store.set("ImageCode:"+imageCodeId,text,constants.IMAGE_CODE_REDIS_EXPIRES)
    #     把生成的验证码放在浏览器上面


    except Exception as e:
        current_app.logger.error(e)
        abort(500)
        # 然后将验证码发给前端(不懂)
    response = make_response(image)
    # response中的image是字符串,需要将image转换成二进制

    response.headers['Content-Type'] = 'image/jpg'
    return response
# 图片发过去了,在哪里取的text


