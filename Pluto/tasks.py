from flask import Blueprint, request, session
from Pluto.models import Task, db

bp=Blueprint('tasks', __name__, url_prefix='/tasks')

@bp.route('/add', methods=['POST'])
def add():
	if validate(request.form):
		task=Task(name=request.form['task'], user_id=session['user_id'], project_id=request.form['project_id'])
		db.session.add(task)
		db.session.commit()
		return 'success'
	else:
		return 'error'


def validate(formData):
	if len(formData['task']) < 5:
		return False

	return True