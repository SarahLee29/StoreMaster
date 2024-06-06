from flask import Blueprint, current_app, flash, jsonify, make_response, redirect, render_template,request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
import jwt
from . import db, create_app
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
    # authen = request.get_json()
    email=request.form.get("email")
    password=request.form.get("password")
    remember = True if request.form.get('remember') else False
    
    # if not authen or not authen.get('email') or not authen.get('password'):
    #     return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic-realm= "Login required!"'})

    user=User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    
    token = jwt.encode({'id': user.id}, current_app.config['SECRET_KEY'], 'HS256')
    print("1",user.id)
    login_user(user, remember=remember)
    session['token'] = token
    print(token)
    return redirect(url_for('app.profile',name=current_user.name))

@auth.route('/token', methods=['GET'])
@login_required
def get_token():
    return session["token"]

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