from flask import Blueprint, flash, current_app, render_template, request, session, redirect, url_for
from Pluto.models import User, db
from werkzeug.security import check_password_hash, generate_password_hash
from os.path import join
import time
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
            UPLOADS_FOLDER=join(current_app.config['BASEDIR'],'pluto','static','images','Users')
            filename = str(time.time()) + secure_filename(image.filename)
            image.save(join(UPLOADS_FOLDER, filename))
            user.avatar = filename
            
        db.session.commit()
        flash('Details updated!', 'success')
        return redirect(request.form['url'])
    else:
        return redirect(url_for('index'))


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
