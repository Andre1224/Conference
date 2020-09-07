#encoding:utf8
from flask import Flask,render_template,request,redirect,url_for,session,g,jsonify
import config
from models import User,Question,Comment
from extension import db
from decorator import login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,and_
from functools import wraps

app = Flask(__name__)
app.config.from_object(config)

# #装饰器,已模块化至decorator
# def login_required(func):
#
#     @wraps(func)        #wraps还原函数__name__，防止装饰器链式重命名问题
#     def wrapper(*args, **kwargs):
#         if session.get('user_id'):
#             return func(*args, **kwargs)
#         else:
#             return redirect(url_for('login'))
#     #如果用户已登录则跳转原地址，如果未登录则跳转到登录页面
#     return wrapper


@app.route('/')
def index():

    context = {
        'questions': Question.query.order_by('-create_time').all()
    }

    return render_template('index.html', **context)

@app.route('/login',methods=['GET',"POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        check = request.form.get('check')
        # user = (User.query.filter(or_(User.username == username, User.telephone == username), User.password == password).first())
        user = (User.query.filter(or_(User.username == username, User.telephone == username)).first())
        # user_tele = User.query.filter(User.telephone == username,User.password == password).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            #如果想长时间不需要重新登录
            # print(check)
            if check:
                session.permanent = True
            else:
                session.permanent = False
            return redirect(url_for('index'))
        else:
            return u'用户名或密码错误'

@app.route('/register',methods=['GET',"POST"])
@app.route('/register/',methods=['GET',"POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')

        #手机号码唯一性验证
        user = User.query.filter(User.telephone == telephone).first()
        name = User.query.filter(User.username == username).first()
        if user:
            return u'该手机号码已注册！'
        elif name:
            return u'用户名已存在'
        else:
            # 验证两次密码相同
            if password != repassword:
                return u'两次密码输入不同，请重新输入。'
            else:
                #注册信息写入数据库
                user = User(telephone=telephone,username=username,password=password)
                db.session.add(user)
                db.session.commit()
                #注册成功，跳转到登录页面
                return redirect(url_for('login'))


@app.route('/question',methods=["GET","POST"])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title = title,content = content)

        # user_id = session.get('user_id')
        # user = User.query.filter(User.id == user_id).first()
        # question.author = user

        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>')
def detail(question_id):
    question_detail = Question.query.filter(Question.id == question_id).first()
    context = {
        'comments': Comment.query.filter(Comment.question_id == question_id).all(),
        'num': Comment.query.filter(Comment.question_id == question_id).count()
    }
    return render_template('detail.html',question = question_detail,**context)
    # return jsonify(question_id)



@app.route('/comment',methods=['POST'])
@login_required
def comment():
    #获取评论内容和问题id
    comment = request.form.get('comment')
    question_id = request.form.get('question_id')
    #将评论内容写入Comment模型，返回submit_comment对象
    submit_comment = Comment(content=comment)

    # #获取当前登录用户id
    # user_id = session['user_id']
    # #查询当前用户信息，返回数据命名为user对象
    # user = User.query.filter(User.id == user_id).first()
    # #将user对象对应至comment的author属性
    # submit_comment.author = user

    submit_comment.author = g.user
    #查询当前问题信息，返回数据命名为question对象
    question = Question.query.filter(Question.id == question_id).first()
    #将question对象对应至comment的question属性
    submit_comment.question = question
    #向数据库提交评论
    db.session.add(submit_comment)
    db.session.commit()

    return redirect(url_for('detail', question_id=question_id))

@app.route('/search')
def search():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q), Question.content.contains(q)))
    return render_template('index.html', questions = questions)

@app.route('/logout')
def logout():
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))

@app.before_request
def my_before_requset():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user
# before_requset -> 视图函数 -> context_processor


@app.context_processor
def my_context_processor():
    # user_id = session.get('user_id')
    # if user_id:
    #     user = User.query.filter(User.id == user_id).first()
    #     if user:
    #         return {'user':user}
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}

db.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)