#encoding:utf8
from functools import wraps
from flask import session,redirect,url_for


#装饰器
def login_required(func):

    @wraps(func)        #wraps还原函数__name__，防止装饰器链式重命名问题
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    #如果用户已登录则跳转原地址，如果未登录则跳转到登录页面
    return wrapper
