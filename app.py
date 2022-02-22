"""Blogly application."""

import re
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarenotcool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
  return redirect('/users')

@app.route('/users')
def show_users():
  """Show list of all users from db"""
  users = User.query.all()
  return render_template('users.html', users=users)

@app.route('/users/new', methods=["GET"])
def show_form():
  """Display form to user"""
  return render_template('add-user.html')

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

  return render_template('details.html', user=user)

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

  return render_template('edit.html')

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

