from flask import Blueprint, abort, redirect, render_template, current_app, session, request, url_for, flash
from Pluto.middlewares import authMiddleware
from Pluto.models import Project, Task, Idea, EditIdea, db
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
            return createProject(request.form, request.files['image'])

    return render_template('projects/new.html')


def createProject(formData, image):
    github_link = formData['github_link']
    if github_link == '':
        github_link = None

    project = Project(name=formData['name'], about=formData['about'], user_id=session['user_id'],
                      picture=uploadImage(image), github_link=github_link)
    db.session.add(project)
    db.session.commit()
    flash('Project created successfully', 'success')
    return redirect(url_for('projects.view', id=project.id, slug=project.name.lower().replace(' ', '')))


@bp.route('/idea/<int:id>', methods=('GET', 'POST'))
@authMiddleware
def fromIdea(id):
    idea = Idea.query.get(id)

    if idea is None:
        abort(404)

    if request.method == 'POST':
        if validateProjectInfo(request.form, request.files, True):
            edits = EditIdea.query.filter((EditIdea.idea_id == id)).all()
            for edit in edits:
                db.session.delete(edit)

            db.session.delete(idea)
            return createProject(request.form, request.files['image'])

    return render_template('projects/new-from-idea.html', idea=idea)


@bp.route('/<int:id>/<slug>')
@authMiddleware
def view(id, slug):
    project = Project.query.get(id)

    if project is None:
        abort(404)

    # making sure that the user enters the proper slug
    if project.name.lower().replace(' ', '-') != slug:
        flash('You do not have access', 'error')
        return redirect(url_for('index'))

    # checking if the authenticated user is the project owner
    if project.user_id != session['user_id']:
        flash('You do not have access', 'error')
        return redirect(url_for('index'))

    numCompletedTasks = len(Task.query.filter(
        (Task.project_id == project.id) & (Task.is_completed == True)).all())

    return render_template('projects/view.html', project=project, numCompletedTasks=numCompletedTasks)


@bp.route('')
@authMiddleware
def all():
    projects = Project.query.filter(
        (Project.user_id == session['user_id'])).all()
    return render_template('projects/all.html', projects=projects)


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@authMiddleware
def edit(id):
    project = Project.query.get(id)

    if project is None:
        abort(404)

    if request.method == 'POST':
        if validateProjectInfo(request.form, request.files, False):
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

    # checking if the authenticated user is the project owner
    if project.user_id != session['user_id']:
        flash('You do not have access', 'error')
        return redirect(url_for('index'))

    return render_template('projects/edit.html', project=project)


@bp.route('/delete/<int:id>')
@authMiddleware
def delete(id):
    project = Project.query.get(id)

    if project is None:
        abort(404)

    tasks = Task.query.filter((Task.project_id == project.id)).all()

    for task in tasks:
        db.session.delete(task)

    db.session.delete(project)
    db.session.commit()
    flash('Project deleted!', 'success')

    return redirect(url_for('projects.all'))


@bp.route('/complete/<int:id>')
@authMiddleware
def complete(id):
    project = Project.query.get(id)

    if project is None:
        abort(404)

    if project.is_completed:
        project.is_completed = False
    else:
        project.is_completed = True

    db.session.commit()
    flash('Project updated!', 'success')

    return redirect(url_for('projects.view', id=project.id, slug=project.name.lower().replace(' ','-')))


def validateProjectInfo(form, files, required):
    if len(form['name']) < 5:
        flash('Project name must be at least 5 characters long', 'error')
        return False

    if 'image' not in files:
        flash('Select an appropriate image', 'error')
        return False

    if required is True:
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


def uploadImage(image):
    filename = str(time.time()) + secure_filename(image.filename)
    UPLOADS_FOLDER = join(
        current_app.config['BASEDIR'], 'pluto', 'static', 'images', 'Projects')
    image.save(join(UPLOADS_FOLDER, filename))

    return filename
