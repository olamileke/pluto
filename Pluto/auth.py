import functools
from flask import render_template, Blueprint, current_app, request, flash, session, redirect, url_for, g
from Pluto.models import User, db
from Pluto.middlewares import guestMiddleware
from werkzeug.security import check_password_hash, generate_password_hash
import os
import requests
import string
import random

bp = Blueprint('auth', __name__)
user = None

@bp.route('/signup', methods=('GET', 'POST'))
@guestMiddleware
def signup():
    if request.method == 'POST':
        if validateSignup(request.form):
            token=''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 255)).lower()
            user = User(name=request.form['name'], dev_name=request.form['dev_name'], activation_token=token, email=request.form['email'],
                        password=generate_password_hash(request.form['password']))
            db.session.add(user)
            db.session.commit()
            sendMail(user)
            flash('Registration Successful', 'success')

            return render_template('auth/signup.html')
        else:
            return render_template('auth/signup.html')

        return render_template('auth/signup.html')

    return render_template('auth/signup.html')


def sendMail(user):
    requests.post(current_app.config['MAIL_BASE_URL'],
                  auth=('api', current_app.config['MAIL_API_KEY']),
                  data={"from": "{0} {1}".format(current_app.config['MAIL_FROM'], current_app.config['MAIL_FROM_URL']),
                        "to": [user.email],
                        "subject": 'Activate Your Account',
                        "html": render_template('mail/activate.html', user=user)})


@bp.route('/login', methods=('GET', 'POST'))
@guestMiddleware
def login():
    if request.method == 'POST':
        if validateLogin(request.form):
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        else:
            return render_template('auth/login.html')

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))


def validateSignup(formData):
    error = None

    if len(formData['name']) < 8:
        error = 'Name must be at least 8 characters long'
        flash(error, 'error')
        return False

    if len(formData['dev_name']) < 5:
        error = 'Dev Nickname must be at least 5 characters long'
        flash(error, 'error')
        return False

    if len(formData['password']) < 8:
        error = 'Password must be at least 8 characters long'
        flash(error, 'error')
        return False

    user=User.query.filter((User.email == formData['email'])).first()

    if user is not None:
        error='User exists for specified email'
        flash(error, 'error')
        return False

    user=User.query.filter((User.dev_name == formData['dev_name'])).first()

    if user is not None:
        error='Dev Name is already taken'
        flash(error, 'error')
        return False

    return True


def validateLogin(formData):
    error = None

    if len(formData['identifier']) is 0:
        error = 'Please enter a valid identifier'
        flash(error, 'error')
        return False

    if len(formData['password']) < 8:
        error = 'Password must be at least 8 characters long'
        flash(error, 'error')
        return False

    user = User.query.filter((User.email == formData['identifier']) | (
        User.dev_name == formData['identifier']) & (User.activation_token == None)).first()

    if user is None:
        error = 'Incorrect username or password'
        flash(error, 'error')
        return False
    elif not check_password_hash(user.password, formData['password']):
        error = 'Incorrect username or password'
        flash(error, 'error')
        return False
    elif user.activation_token is not None:
        error = 'Incorrect username or password'
        flash(error, 'error')
        return False
    else:
        session.clear()
        session['user_id'] = user.id
        return True


@bp.before_app_request
def getCurrentUser():
    if 'user_id' in session:
        g.user = User.query.filter(User.id == session['user_id']).first()
    else:
        g.user = None

    g.URL = request.host_url

