"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)

class User(db.Model):
  """User."""
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
                        default="https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png")

  def __repr__(self):
    u = self
    return f'<User id={u.id}, first_name={u.first_name}, last_name={u.last_name}, image_url={u.image_url}>'