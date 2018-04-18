from exits import db
import time
import shortuuid



class User(db.Model):
    __tablename__='user'
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    name =db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Tags(db.Model):
    __tablename__='tags'
    id=db.Column(db.Integer,primary_key=True, autoincrement= True)
    tagname=db.Column(db.String(100),nullable=False)

class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.Date, default=time.strftime('%Y-%m-%d', time.localtime(time.time())))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    tag = db.relationship('Tags',backref=db.backref('articles'))

    __mapper_args__ = {
        'order_by': create_time.desc()
    }


