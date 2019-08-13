from flask import Blueprint, redirect, render_template, current_app, session, request, url_for, flash
from Pluto.middlewares import authMiddleware
from Pluto.models import Project, db
from werkzeug.utils import secure_filename
import time
from os.path import join

bp = Blueprint('projects', __name__, url_prefix='/projects')

allowedExtensions = ['jpg', 'jpeg', 'png']


@bp.route('/new', methods=('GET', 'POST'))
@authMiddleware
def new():
    if request.method == 'POST':
        if validateProjectInfo(request.form, request.files):
            image=request.files['image']
            filename=str(time.time()) + secure_filename(image.filename)
            UPLOADS_FOLDER=join(current_app.config['BASEDIR'], 'pluto', 'static', 'images', 'Projects')
            image.save(join(UPLOADS_FOLDER,filename))

            if request.form['github_link'] == '':
            	request.form['github_link']=None

            project=Project(name=request.form['name'], about=request.form['about'], user_id=session['user_id'],
            				picture=filename,github_link=request.form['github_link'])
            db.session.add(project)
            db.session.commit()
            flash('Project created successfully', 'success')
            return redirect(url_for('projects.new'))

    return render_template('projects/new.html')


@bp.route('/<int:id>/<slug>')
@authMiddleware
def view(id, slug):
    project=Project.query.filter((Project.id == id)).first()
    return render_template('projects/view.html', project=project)



def validateProjectInfo(form, files):
    if len(form['name']) < 5:
        flash('Project name must be at least 5 characters long', 'error')
        return False

    if 'image' not in files:
        flash('Select an appropriate image', 'error')
        return False

    image = files['image']

    if image.filename == '':
        flash('Select an appropriate image', 'error')
        return False

    extension = image.filename.rsplit('.')[1].lower()

    if extension not in allowedExtensions:
        flash('File format is not supported', 'error')
        return False

    if len(form['about']) < 5:
        flash('Project description must be at least 5 characters long', 'error')
        return False

    return True
