from flask import Blueprint, flash, current_app, render_template, request, session, redirect, url_for
from Pluto.models import User, db, PasswordReset
from Pluto.middlewares import guestMiddleware
from werkzeug.security import check_password_hash, generate_password_hash
from os.path import join
import time
import requests
import string
import random
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/update', methods=['POST'])
def update():
    if validate(request.form):
        user = User.query.filter((User.id == session['user_id'])).first()

        if len(request.form['name']) > 0:
            user.name = request.form['name']

        if len(request.form['dev_name']) > 0:
            user.dev_name = request.form['dev_name']

        if len(request.form['password']) > 0:
            user.password = generate_password_hash(request.form['password'])

        image = request.files['image']

        if image.filename != '':
            UPLOADS_FOLDER = join(
                current_app.config['BASEDIR'], 'pluto', 'static', 'images', 'Users')
            filename = str(time.time()) + secure_filename(image.filename)
            image.save(join(UPLOADS_FOLDER, filename))
            user.avatar = filename

        db.session.commit()
        flash('Details updated!', 'success')
        return redirect(request.form['url'])
    else:
        return redirect(url_for('index'))


@bp.route('/send_password_reset_mail', methods=['POST'])
def sendPasswordResetMail():
    user = User.query.filter((User.email == request.form['email'])).first()

    if user is None:
        return 'error'

    token = ''.join(random.choices(string.ascii_uppercase +
                                   string.digits, k=200)).lower()

    expiry = datetime.now() + timedelta(minutes=30)

    reset = PasswordReset(
        user_id=user.id, reset_token=token, time_expiry=expiry)
    db.session.add(reset)
    db.session.commit()

    sendMail(user, expiry, token)

    return 'success'


def sendMail(user, expiry, token):
    requests.post(current_app.config['MAIL_BASE_URL'],
                  auth=('api', current_app.config['MAIL_API_KEY']),
                  data={"from": "{0} {1}".format(current_app.config['MAIL_FROM'], current_app.config['MAIL_FROM_URL']),
                        "to": [user.email],
                        "subject": 'Reset Your Password',
                        "html": render_template('mail/password_reset.html', user=user, expiry=expiry, token=token)})


@bp.route('/reset_password/<token>', methods=('GET', 'POST'))
@guestMiddleware
def resetPassword(token):
    reset = PasswordReset.query.filter(
        (PasswordReset.reset_token == token)).first()

    if reset is None:
        flash('Invalid reset token!', 'error')
        return redirect(url_for('auth.login'))

    now = datetime.now()

    if now > reset.time_expiry:
        flash('Expired reset token', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        if len(request.form['password']) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return redirect(url_for('user.resetPassword', token=token))

        hashedPassword = generate_password_hash(request.form['password'])
        user = User.query.get(reset.user_id)
        user.password = hashedPassword
        db.session.delete(reset)
        db.session.commit()

        flash('Password changed successfully!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', token=token)


def validate(formData):
    if len(formData['name']) > 0:
        if len(formData['name']) < 5:
            flash('Name must be at least 5 characters long', 'error')
            return False

    if len(formData['dev_name']) > 0:
        if len(formData['dev_name']) < 5:
            flash('Dev name must be at least 5 characters long', 'error')
            return False

    if len(formData['password']) > 0:
        if len(formData['password']) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return False

    return True
