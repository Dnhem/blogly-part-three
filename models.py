"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

DEFAULT_IMG_URL = "https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png"

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)

class User(db.Model):
  """User Model"""
  __tablename__ = 'users'

  id = db.Column(db.Integer, 
                 primary_key=True,
                 autoincrement=True)
  
  first_name = db.Column(db.String(50),
                         nullable=False,
                         unique=True)

  last_name = db.Column(db.String(50),
                         nullable=False,
                         unique=True)

  image_url = db.Column(db.String,
                        nullable=False,
                        default=DEFAULT_IMG_URL)

  posts = db.relationship('Post', backref='user')

  def __repr__(self):
    u = self
    return f'<User_id={u.id}, first_name={u.first_name}, last_name={u.last_name}, image_url={u.image_url}>'

  @property
  def full_name(self):
    return f'{self.first_name} {self.last_name}'

class Post(db.Model):
  """Post Model"""

  __tablename__ = 'posts'

  id = db.Column(db.Integer,
                 primary_key=True,
                 autoincrement=True)

  title = db.Column(db.String(50),
                    nullable=False,
                    )

  content = db.Column(db.String,
                      nullable=False)

  created_at = db.Column(db.DateTime,
                         nullable=False,
                         default=datetime.datetime.now)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  def __repr__(self):
    return f'<Post id={self.id}, Post Title={self.title}, Post Content={self.content}, User Id={self.user_id}>'

class PostTag(db.Model):

  __tablename__='post_tag'

  post_id = db.Column(db.Integer, 
                      db.ForeignKey('posts.id'),
                      primary_key=True)
                      
  tag_id = db.Column(db.Integer,
                     db.ForeignKey('tags.id'),
                     primary_key=True)

  def __repr__(self):

    return f'<Post id={self.post_id}, Tag id={self.tag_id}>'

class Tag(db.Model):

  __tablename__ = 'tags'

  id = db.Column(db.Integer, 
                 primary_key=True,
                 autoincrement=True)

  name = db.Column(db.String(20),
                   nullable=False,
                   unique=True)

  posts = db.relationship('Post', 
                          secondary='post_tag',
                          backref='tags')

  def __repr__(self):
    return f'<Tag id = {self.id}, Tag name = {self.name}>'



