from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

class User(UserMixin,db.Model):
    __tablename__ = 'users'


    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    pitch = db.relationship('Pitch',backref='user',lazy="dynamic")
    comment_id = db.relationship('Comment',backref = 'list',lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)   


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def __repr__(self):
        return f'User {self.username}'

class Category(db.Model):
    '''
    Class will hold te category items
    '''
    __tablename__ = 'categories'
    id = db.Column(db.Integer,primary_key = True)
    category = db.Column(db.String(255))
    

    def __repr__(self):
        return f'User {self.name}'

class Pitch(db.Model):
    
    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    category_name = db.Column(db.String(255))
    comments = db.relationship('Comment',backref= 'pitch',lazy="dynamic")
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    pitch_content = db.Column(db.String(255))
    upVote = db.Column(db.Integer,default= 0 )
    downVote= db.Column(db.Integer,default = 0)

    def __repr__(self):
        return f'User {self.name}'
      

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    user = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    com_write = db.Column(db.String(255))    

    def __repr__(self):
        return f'User {self.name}'