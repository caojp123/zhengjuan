from django.http import JsonResponse
from zhengquan.settings import REDIS, MAIL_SMTP, \
    MAIL_SENDER, MAIL_LICENSE, SALT, DATABASE
from login_register.send_email_model import SendEmail
from login_register.tools_model import ToolsModel
from login_register.models import UserInfo

# 创建邮件发送对象
sendEmail = SendEmail(MAIL_SMTP, MAIL_SENDER, MAIL_LICENSE)
# 创建工具类对象
tools = ToolsModel()
# 创建用户存储类
userInfo = UserInfo(DATABASE)


# 用户注册逻辑
def register_logic(request):
    params = request.POST
    name = params.get('name')
    password = params.get('password')
    email = params.get('email')
    code = params.get('code')
    if tools.check_code(email,code):
        return JsonResponse({'error': 1, 'reason': 'code验证失败！'})
    if tools.check_name(name):
        return JsonResponse({'error': 1, 'reason': '用户名格式有误！'})
    if tools.check_pwd(password):
        return JsonResponse({'error': 1, 'reason': '密码格式有误！'})
    name_status = userInfo.search_name(name=name)
    if name_status:
        return JsonResponse({'error': 1, 'reason': '用户名已存在！'})
    password = tools.data_enc(password, SALT)
    save_status = userInfo.save_user_info(name=name,password=password, email=email)
    if save_status:
        token = tools.create_token(name=name, salt=SALT)
        return JsonResponse({'error': 0, 'reason': '注册成功!', 'token': token})
    else:
        return JsonResponse({'error': 1, 'reason': '注册失败!', 'token': ''})


# 用户登录逻辑
def login_logic(request):
    pass


# 生成验证码
def get_code(request):
    email = request.POST.get('email', 'none')
    if not tools.check_email(email):
        return JsonResponse({'error': 1, 'reason': '邮箱格式有误！'})
    code = tools.create_code()
    data = sendEmail.send_email(email, code)
    if data.get('error') == 0:
        REDIS.set(email, code, 60*5)
    return JsonResponse(data)

