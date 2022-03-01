"""Blogly application."""

from crypt import methods
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Post, PostTag, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "chickenzarenotcool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# Blogly Part 1 (Users)

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

# Blogly Part 2 (Posts)

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
  """Render page to allow user to post new entry with form"""

  user = User.query.get_or_404(user_id)

  tags = Tag.query.all()

  return render_template('posts/post-form.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_form(user_id):

  user = User.query.get_or_404(user_id)
  new_post = Post(title=request.form['title'],
                  content=request.form['content'],
                  user=user)

  tags = request.form.getlist('tag')
  print(tags)

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

# Blogly Part 3 (Tags)

@app.route('/tags')
def list_tags():
  """Fetch all tags from database and render on page"""
  all_tags = db.session.query(Tag).all()

  return render_template('/tags/list-tags.html', all_tags=all_tags)

@app.route('/tags', methods=["POST"])
def post_tag():
  """Create new tag and add to database"""
  tag_name = request.form["tag"]
  new_tag = Tag(name=tag_name)
  db.session.add(new_tag)
  db.session.commit()

  all_tags = db.session.query(Tag).all()

  return render_template('/tags/list-tags.html', all_tags=all_tags)
  
@app.route('/tags/<int:tag_id>')
def show_tags(tag_id):

  show_tag = Tag.query.get_or_404(tag_id)

  return render_template('tags/show-tags.html', show_tag=show_tag)

@app.route('/tags/new')
def new_tag():
  return render_template('tags/new-tag.html')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
  """Show edit tag form"""
  return render_template('tags/edit.html')

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
  """Edit tag form in database"""
  tag = Tag.query.get(tag_id)

  edit_tag = request.form["edit-tag"]
  tag.name = edit_tag
  db.session.add(tag)
  db.session.commit()

  return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
  
  tag = Tag.query.get(tag_id)

  db.session.delete(tag)
  db.session.commit()

  return redirect('/tags')