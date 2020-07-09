# coding: utf-8
import re
import jwt
import time
import random
import hashlib
from zhengquan.settings import REDIS


class ToolsModel:
    def __init__(self):
        pass

    # 检测用户名
    @staticmethod
    def check_name(name):
        # 用户名由1-6个字符组成，且不能含有空白字符。
        parent = '^\S{1,6}$'
        if re.findall(parent, name):
            return True
        else:
            return False

    # 检测用户密码
    @staticmethod
    def check_pwd(password):
        parent = '^[0-9A-Za-z.?!*&%,$#@]{6,16}$'
        if re.findall(parent, password):
            return True
        else:
            return False

    # 检测用户邮箱
    @staticmethod
    def check_email(email):
        parent = '^[0-9A-Za-z]+@[0-9a-zA-Z]+\.com$'
        if re.findall(parent, email):
            return True
        else:
            return False

    # 创建身份验证的token
    @staticmethod
    def create_token(name, salt):
        payload = {
            # token 的过期时间
            'exp': time.time() + 30*24*60*60,
            'name': name,
            'season': 1
        }
        return jwt.encode(payload=payload, key=salt).decode()

    # 解析token中的数据
    @staticmethod
    def pars_token(token, salt):
        try:
            payload = jwt.decode(token, salt)
            return payload
        except:
            return None

    # 创建code字符串
    @staticmethod
    def create_code():
        char_list = [str(random.randint(1, 10)) for i in range(4)]
        code = ''.join(char_list)
        return code

    # 检测code正确性(测试)
    @staticmethod
    def check_code(email, code):
        past_code = REDIS.get(email)
        if past_code and past_code.decode() == code:
            return True
        else:
            return False

    # 数据加密
    @staticmethod
    def data_enc(data, salt):
        md5 = hashlib.md5()
        md5.update(data.encode())
        data = md5.hexdigest() + salt
        md5 = hashlib.md5()
        md5.update(data.encode())
        return md5.hexdigest()

