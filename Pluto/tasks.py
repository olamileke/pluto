from flask import Blueprint, request, session
import json
from Pluto.models import Task, db
from datetime import datetime

bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@bp.route('/add', methods=['POST'])
def add():
    if validate(request.form):
        task = Task(name=request.form['task'], user_id=session['user_id'],
                    project_id=request.form['project_id'])
        db.session.add(task)
        db.session.commit()
        return str(task.id)
    else:
        return 'error'


@bp.route('/update', methods=['POST'])
def update():
    tasks = json.loads(request.form['tasks'])

    for k in tasks:
        task = Task.query.get(k)

        if tasks[k]:
            task.is_completed = True
            task.completed_at = datetime.utcnow()
        else:
            task.is_completed = False
            task.completed_at = None

        db.session.commit()

    return 'success'


def validate(formData):
    if len(formData['task']) < 5:
        return False

    return True
