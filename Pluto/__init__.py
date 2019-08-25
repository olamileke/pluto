import os
from flask import Flask, render_template, session, request
from flask_migrate import Migrate
from . import auth
from . import projects
from . import ideas
from . import user
from . import tasks
from .middlewares import authMiddleware
from datetime import timedelta


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_SETTINGS'))
    # app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:Arsenalfc@localhost:5432/pluto"
    app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=14)
    app.secret_key = os.urandom(16)

    from . import models

    models.db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, models.db)
    app.register_blueprint(auth.bp)
    app.register_blueprint(projects.bp)
    app.register_blueprint(ideas.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(tasks.bp)

    @app.before_request
    def setPermanentSession():
        session.permanent=True

    @app.route('/')
    def index():
        if 'user_id' in session:
            projects = models.Project.query.filter((models.Project.user_id == session['user_id']) & (
                models.Project.is_completed == False)).all()
            return render_template('auth_index.html', projects=projects)

        return render_template('index.html')

    @app.route('/search')
    @authMiddleware
    def search():
        term=request.args.get('term')
        search="%{}%".format(term)

        projects=models.Project.query.filter(((models.Project.name.ilike(search)) | (models.Project.about.ilike(search))) & (models.Project.user_id == session['user_id'])).all()
        ideas=models.Idea.query.filter(((models.Idea.name.ilike(search)) | (models.Idea.premise.ilike(search))) & (models.Idea.user_id == session['user_id'])).all()
        length=len(projects) + len(ideas)

        return render_template('search.html', term=term, projects=projects, ideas=ideas, length=length)

    return app
