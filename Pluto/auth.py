from flask import render_template, Blueprint, request, flash
from Pluto.models import User, db
from werkzeug.security import check_password_hash, generate_password_hash
import os

bp = Blueprint('auth', __name__)


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        if validate(request.form):
            user = User(name=request.form['name'], dev_name=request.form['dev_name'], email=request.form['email'],
                        password=generate_password_hash(request.form['password']))
            db.session.add(user)
            db.session.commit()

            flash('Registration Successful', 'success')
            return render_template('auth/signup.html')
        else:
            return render_template('auth/signup.html')

    return render_template('auth/signup.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        print('leke')

    return render_template('auth/login.html')


def validate(formData):
    error = None

    if len(formData['name']) < 8:
        error = 'Name must be at least 8 characters long'
        flash(error, 'danger')
        return False

    if len(formData['dev_name']) < 5:
        error = 'Dev Nickname must be at least 5 characters long'
        flash(error, 'danger')
        return False

    if len(formData['password']) < 8:
        error = 'Password must be at least 8 characters long'
        flash(error, 'danger')
        return False

    return True
