from flask import Blueprint, redirect, render_template, request, url_for, flash
from Pluto.middlewares import authMiddleware

bp=Blueprint('projects', __name__, url_prefix='/projects')

@bp.route('/new', methods=('GET', 'POST'))
@authMiddleware
def new():
	if request.method == 'POST':
		pass

	return render_template('projects/new.html')


