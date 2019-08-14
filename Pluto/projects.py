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
        if validateProjectInfo(request.form, request.files, True):

            github_link = request.form['github_link']
            if github_link == '':
                github_link = None

            project = Project(name=request.form['name'], about=request.form['about'], user_id=session['user_id'],
                              picture=uploadImage(request.files['image']), github_link=github_link)
            db.session.add(project)
            db.session.commit()
            flash('Project created successfully', 'success')
            return redirect(url_for('projects.new'))

    return render_template('projects/new.html')


@bp.route('/<int:id>/<slug>')
@authMiddleware
def view(id, slug):
    project = Project.query.filter((Project.id == id)).first()

    # checking if the authenticated user is the project owner
    if project.user_id != session['user_id']:
        flash('You do not have access', 'error')
        return redirect(url_for('index'))

    return render_template('projects/view.html', project=project)


@bp.route('')
@authMiddleware
def all():
    projects = Project.query.filter(
        (Project.user_id == session['user_id'])).all()
    return render_template('projects/all.html', projects=projects)


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@authMiddleware
def edit(id):
    if request.method == 'POST':
        if validateProjectInfo(request.form, request.files, False):
            project = Project.query.filter((Project.id == id)).first()

            project.name = request.form['name']
            project.about = request.form['about']
            github_link = request.form['github_link']

            if github_link == '':
                github_link = None

            project.github_link = github_link

            if request.files['image'].filename != '':
                project.picture = uploadImage(request.files['image'])

            db.session.commit()
            flash('Project updated!', 'success')
            return redirect(url_for('projects.view', id=id, slug=project.name.lower().replace(' ', '-')))

    project=Project.query.filter((Project.id == id)).first()

    # checking if the authenticated user is the project owner
    if project.user_id != session['user_id']:
        flash('You do not have access', 'error')
        return redirect(url_for('index'))

    return render_template('projects/edit.html', project=project)


def validateProjectInfo(form, files, required):
    if len(form['name']) < 5:
        flash('Project name must be at least 5 characters long', 'error')
        return False

    if 'image' not in files:
        flash('Select an appropriate image', 'error')
        return False

    if required is True:
        image=files['image']

        if image.filename == '':
            flash('Select an appropriate image', 'error')
            return False

        extension=image.filename.rsplit('.')[1].lower()

        if extension not in allowedExtensions:
            flash('File format is not supported', 'error')
            return False

    if len(form['about']) < 5:
        flash('Project description must be at least 5 characters long', 'error')
        return False

    return True


def uploadImage(image):
    filename=str(time.time()) + secure_filename(image.filename)
    UPLOADS_FOLDER=join(
        current_app.config['BASEDIR'], 'pluto', 'static', 'images', 'Projects')
    image.save(join(UPLOADS_FOLDER, filename))

    return filename
