from flask import Blueprint, flash, redirect, render_template,request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login')
# @login_required # prevent users not logged in from seeing the route
def login():
    if current_user.is_authenticated:
        return redirect(url_for('app.profile',name=current_user.name))
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email=request.form.get("email")
    password=request.form.get("password")
    remember = True if request.form.get('remember') else False
    print("remember",remember)

    user=User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    print("redirect")
    print(current_user.name)
    return redirect(url_for('app.profile',name=current_user.name))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup',methods=['POST'])
def signup_post():
    print("regi")
    email=request.form.get("email")
    password=request.form.get("password")
    name=request.form.get("name")

    user=User.query.filter_by(email=email).first()
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2',salt_length=16))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required  #only logged in users can see this route
def logout():
    logout_user()
    return redirect(url_for('app.index'))