"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "chickenzarenotcool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# Blogly Part 1

@app.route('/')
def homepage():
  return redirect('/users')

@app.route('/users')
def show_users():
  """Show list of all users from db"""
  users = User.query.all()
  return render_template('/users/users.html', users=users)

@app.route('/users/new', methods=["GET"])
def show_form():
  """Display form to user"""
  return render_template('/users/add-user.html')

@app.route('/users/new', methods=["POST"])
def add_new_user():
  """Add new user"""

  first_name = request.form['firstname']
  last_name = request.form['lastname']
  image_url = request.form['imageurl'] or None

  new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
  db.session.add(new_user)
  db.session.commit()

  return redirect('/users')

@app.route('/users/<int:user_id>')
def user_details(user_id):
  """Show user profile"""
  user = User.query.get_or_404(user_id)

  return render_template('/users/details.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
  """Delete User"""

  user = User.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit()

  return redirect('/users')

@app.route('/users/<int:user_id>/edit', methods=["GET"])
def show_edit_form(user_id):
  """Show edit form"""

  return render_template('/users/edit.html')

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
  """Edit User"""

  user = User.query.get_or_404(user_id)

  user.first_name = request.form['firstname']
  user.last_name = request.form['lastname']
  user.image_url = request.form['imageurl']

  db.session.add(user)
  db.session.commit()

  return redirect('/users')

# Blogly Part 2

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):

  user = User.query.get_or_404(user_id)
  return render_template('posts/post-form.html', user=user)
# Render page to allow user to post new entry with form

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_form(user_id):

  user = User.query.get_or_404(user_id)
  new_post = Post(title=request.form['title'],
                  content=request.form['content'],
                  user=user)
  
  db.session.add(new_post)
  db.session.commit()

  return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):

  post = Post.query.get_or_404(post_id)

  return render_template('posts/post.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):

  post = Post.query.get_or_404(post_id)

  return render_template('posts/edit-post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):

  post = Post.query.get_or_404(post_id)
  post.title = request.form['title']
  post.content = request.form['content']

  db.session.add(post)
  db.session.commit()

  return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):

  post = Post.query.get_or_404(post_id)

  db.session.delete(post)
  db.session.commit()

  return redirect(f'/users/{post.user_id}')