from flask import Blueprint, redirect, render_template, request, url_for, flash
from Pluto.middlewares import authMiddleware
from Pluto.models import Project, db

bp=Blueprint('projects', __name__, url_prefix='/projects')

allowedExtensions=['jpg','jpeg','png']

@bp.route('/new', methods=('GET', 'POST'))
@authMiddleware
def new():
	if request.method == 'POST':
		if validateProjectInfo(request.form, request.files):
			pass


	return render_template('projects/new.html')


def validateProjectInfo(form, files):
	if len(form['name']) < 5:
		flash('Project name must be at least 5 characters long', 'error')
		return False

	if 'image' not in files:
		flash('Select an appropriate image', 'error');
		return False

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


