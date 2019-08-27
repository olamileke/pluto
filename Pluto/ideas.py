from flask import Blueprint, abort, redirect, url_for, request, session, flash, render_template
from Pluto.models import Idea, db, EditIdea
from Pluto.middlewares import authMiddleware

bp = Blueprint('ideas', __name__, url_prefix='/ideas')


@bp.route('/new', methods=('GET', 'POST'))
@authMiddleware
def new():
    if request.method == 'POST':
        if validate(request.form):
            idea = Idea(
                name=request.form['name'], user_id=session['user_id'], premise=request.form['premise'])
            db.session.add(idea)
            db.session.commit()
            flash('Idea added successfully', 'success')
            return redirect(url_for('ideas.view', id=idea.id, slug=idea.name.lower().replace(' ','-')))

    return render_template('ideas/new.html')


@bp.route('')
@authMiddleware
def all():
    ideas = Idea.query.filter((Idea.user_id == session['user_id'])).all()

    return render_template('ideas/all.html', ideas=ideas)


@bp.route('/<int:id>/<slug>')
@authMiddleware
def view(id, slug):
    idea = Idea.query.get(id)

    if idea is None:
        abort(404)

    # making sure that the slug is correct
    if idea.name.lower().replace(' ', '-') != slug:
        flash('You do not have access', 'error')
        return redirect(url_for('index'))

    # checking if the creator of the idea is the authenticated user
    if idea.user_id != session['user_id']:
        flash('You do not have access', 'error')
        return redirect(url_for('index'))

    return render_template('ideas/view.html', idea=idea)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@authMiddleware
def edit(id):
    idea = Idea.query.get(id)

    if idea is None:
        abort(404)

    # checking if the creator of the idea is the authenticated user
    if idea.user_id != session['user_id']:
        flash('You do not have access', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        if validate(request.form):
            if idea.name.replace(' ', '') != request.form['name'].replace(' ', '') and idea.premise.replace(' ', '') != request.form['premise'].replace(' ', ''):
                saveEdit(db, idea.id, 'Edit name', request.form['name'])
                saveEdit(db, idea.id, 'Edit premise', request.form['premise'])

            elif idea.name.replace(' ', '') != request.form['name'].replace(' ', ''):
                saveEdit(db, idea.id, 'Edit name', request.form['name'])

            elif idea.premise.replace(' ', '') != request.form['premise'].replace(' ', ''):
                saveEdit(db, idea.id, 'Edit premise', request.form['premise'])

            idea.name = request.form['name']
            idea.premise = request.form['premise']

            db.session.commit()
            flash('Idea updated!', 'success')
            return redirect(url_for('ideas.view', id=idea.id, slug=idea.name.lower().replace(' ', '-')))
        else:
            return render_template('ideas/edit.html', idea=idea)

    return render_template('ideas/edit.html', idea=idea)


@bp.route('/delete/<int:id>')
@authMiddleware
def delete(id):
    idea=Idea.query.get(id)

    if idea is None:
        abort(404)

    db.session.delete(idea)
    db.session.commit()
    flash('Idea deleted!', 'success')
    return redirect(url_for('ideas.all'))


def saveEdit(db, id, act, res):
    edit = EditIdea(idea_id=id, action=act, result=res)
    db.session.add(edit)
    db.session.commit()


def validate(form):
    if len(form['name']) < 5:
        flash('Name field must be at least 5 characters long', 'error')
        return False

    if len(form['premise']) < 5:
        flash('Premise field must be at least 5 characters long', 'error')
        return False

    return True
