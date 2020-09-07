#encoding:utf-8
import os

DEBUG = True
HOST = '0.0.0.0'

SECRET_KEY = os.urandom(24)

# 数据库配置
HOSTNAME='127.0.0.1'
PORT='3306'
DATABASE='test'
USERNAME='root'
PASSWORD='000000'
DB_URI='mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI=DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS=False