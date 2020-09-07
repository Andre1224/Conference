from extension import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self,*args,**kwargs):
        telephone = kwargs.get('telephone')
        username  = kwargs.get('username')
        password  = kwargs.get('password')

        self.telephone = telephone
        self.username = username
        #密码加密
        self.password = generate_password_hash(password)

    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    #now()会保存服务首次运行时间,now为内次运行时的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref = db.backref('questions'))

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.TEXT,nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

    question = db.relationship('Question', backref = db.backref('comments'))
    author = db.relationship('User', backref = db.backref('comments'))