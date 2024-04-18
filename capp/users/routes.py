from flask import render_template, Blueprint, redirect, flash, url_for, request
from capp.users.forms import Register, Login
from capp.models import User
from capp import db, bcrypt
from flask_login import login_user, current_user, logout_user

users=Blueprint('users',__name__)

@users.route('/register', methods=['GET','POST'])
def register():
  form = Register()
  if current_user.is_authenticated:
        return redirect(url_for('home.home_home'))
  if form.validate_on_submit():
      user_hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      user = User(username=form.username.data, email=form.email.data, password=user_hashed_password)
      db.session.add(user)
      db.session.commit()
      flash('Your account has been created! ✅ Now, you are able to login.', 'success')
      return redirect(url_for('users.login'))
  return render_template('users/register.html', title='register', form=form)

@users.route('/login', methods=['GET','POST'])
def login():
  form = Login()
  if current_user.is_authenticated:
        return redirect(url_for('home.home_home'))
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        flash('You have been logged in successfully 🌍 The carbon calculator is ready for use!', 'success')
        return redirect(next_page) if next_page else redirect(url_for('home.home_home'))
    else:
        flash('Login unsuccessful ❌ Please check email and password!', 'danger') 
  return render_template('users/login.html', title='login', form=form)

@users.route('/logout')
def logout():    
    logout_user()
    flash('You have been logged out 👋🏾', 'success')
    return redirect(url_for('home.home_home'))
