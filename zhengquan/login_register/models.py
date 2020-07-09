# from django.db import models
import threading


# Create your models here.
class UserInfo:
    def __init__(self, database=None):
        self.__dataBase = database

    # 检测用户名是否存在
    def search_name(self, name):
        sql = 'select name from user where name=%s'
        cursor = self.__dataBase.cursor()
        cursor.execute(sql,[name])
        if cursor.fetchone():
            return True
        else:
            return False

    # 保存用户信息
    def save_user_info(self, name, password, email):
        try:
            sql = 'insert into user(name, password, email)values(%s, %s, %s)'
            cursor = self.__dataBase.cursor()
            cursor.execute(sql, [name, password, email])
            self.__dataBase.commit()
            return True
        except:
            print('用户信息存储失败！')
            return False
