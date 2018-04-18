import flask
from flask import Flask
from exits import db
from models import User,Tags,Articles
import os
from sqlalchemy import or_
# from forms import ArticleForm
# from flask_pagedown import PageDown
# from flask_ckeditor import CKEditor

app = Flask(__name__)
# pageDown = PageDown(app)
# pageDown.init_app(app)


# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/blog'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True # 自动更新变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# 配置debug
app.config['DEBUG']= True
#配置session
app.config['SECRET_KEY'] = os.urandom(24)



@app.route('/',methods=['GET','POST'])
def index():
    page = flask.request.args.get('page', 1, type=int)
    pagination=Articles.query.order_by('-create_time').paginate(
        page,per_page=3,
        error_out=False
    )
    articles=pagination.items
    return flask.render_template('index.html', articles=articles,pagination=pagination)
    # context = {
    #     'articles': Articles.query.order_by('-create_time').all()
    # }
    # return flask.render_template('index.html',**context)
# @app.route('/class/')
# def class():
#     class=Tags.query.filterl

@app.route('/about/')
def about():
    return flask.render_template('about.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    else:
        name = flask.request.form.get('name')
        password = flask.request.form.get('password')
        user = User.query.filter(User.name == name, User.password == password).first()
        if user:
            flask.session['id'] = user.id
            return flask.redirect(flask.url_for('index'))
        else:
            flask.flash("登陆失败")
            return flask.redirect(flask.url_for('login'))

@app.route('/article/<id>')
def article(id):
    article=Articles.query.filter(Articles.id==id).first()
    return flask.render_template('article.html',article=article)



@app.route('/publish/',methods=['GET','POST'])
def publish():
    user_id=flask.session.get('id')
    if user_id:
        if flask.request.method=='GET':
            return flask.render_template('publish.html')
        else:
            title=flask.request.form.get('title')
            content=flask.request.form.get('content')
            tagname=flask.request.form.get('tagname')
            id=flask.request.form.get('id')
            tag=Tags.query.filter(Tags.tagname==tagname).first()
            if tag:
                tag_id=tag.id
            else:
                tag=Tags(tagname=tagname)
                db.session.add(tag)
                db.session.commit()
                tag_id = Tags.query.filter(Tags.tagname == tagname).first().id
            article=Articles(id=id,title=title,content=content,tag_id=tag_id)
            db.session.add(article)
            db.session.commit()
            return flask.redirect(flask.url_for('index'))
            # title = form.title.data
            # content = form.content.data
            # tagname = form.tagname.data
            # tag = Tags.query.filter(Tags.tagname == tagname).first()
            # if tag:
            #     tag_id = tag.id
            # else:
            #     tag=Tags(tagname=tagname)
            #     db.session.add(tag)
            #     db.session.commit()
            #     tag_id = Tags.query.filter(Tags.tagname == tagname).first().id
            # article=Articles(title=title,content=content,tag_id=tag_id)
            # db.session.add(article)
            # db.session.commit()
            # return flask.redirect(flask.url_for('index'))
    else:
        return flask.redirect(flask.url_for('login'))

@app.route('/search/')
def search():
    q = flask.request.args.get('q')
    articles = Articles.query.order_by('-create_time').filter(or_(Articles.title.contains(q), Articles.content.contains(q)))
    context = {
        'articles': articles
    }
    return flask.render_template('index.html', **context)


@app.route('/edit/<article_id>',methods=['GET','POST'])
def edit(article_id):
    user_id=flask.session.get('id')
    if user_id:
        article=Articles.query.filter(Articles.id==article_id).first()
        tag=Tags.query.filter(Tags.id==article.tag_id).first()
        if flask.request.method=='GET':
            context={
                'article': article,
                'tag':tag
            }
            print(article.content)
            return flask.render_template('edit.html',**context)
        else:
            title=flask.request.form.get('title')
            content=flask.request.form.get('content')
            tagname=flask.request.form.get('tagname')
            id = flask.request.form.get('id')
            tag=Tags.query.filter(Tags.tagname==tagname).first()
            if tag:
                tag_id=tag.id
            else:
                tag=Tags(tagname=tagname)
                db.session.add(tag)
                db.session.commit()
                tag_id=Tags.query.filter(Tags.tagname==tagname).first().id
            article.id=id
            article.title=title
            article.content=content
            article.tag_id=tag_id
            db.session.commit()
            return flask.redirect(flask.url_for('index'))
    else:
        return flask.redirect(flask.url_for('login'))

@app.context_processor
def my_context_processor():
    user_id = flask.session.get('id')
    if user_id:
        user = User.query.filter(User.id==user_id).first()
        if user:
            return {'user':user}
    return {}

if __name__ == '__main__':
    app.run(debug=True)
