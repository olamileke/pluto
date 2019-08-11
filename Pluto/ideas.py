from flask import Blueprint, redirect, url_for, request, session, flash, render_template
from Pluto.models import Idea, db
from Pluto.middlewares import authMiddleware

bp=Blueprint('ideas', __name__, url_prefix='/ideas')

@bp.route('/new', methods=('GET', 'POST'))
@authMiddleware
def new():
	if request.method == 'POST':
		if validate(request.form):
			idea=Idea(name=request.form['name'], user_id=session['user_id'], premise=request.form['premise'])
			db.session.add(idea)
			db.session.commit()
			flash('Idea added successfully', 'success')
			return redirect(url_for('ideas.new'))

	return render_template('ideas/new.html')


def validate(form):
	if len(form['name']) < 5:
		flash('Name field must be at least 5 characters long', 'error')
		return False

	if len(form['premise']) < 5:
		flash('Premise field must be at least 5 characters long', 'error')
		return False

	return True

