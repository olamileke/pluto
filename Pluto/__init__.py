import os
from flask import Flask, render_template, session
from flask_migrate import Migrate
from . import auth
from . import projects
from . import ideas

migrate=Migrate()

def create_app(test_config=None):
	app=Flask(__name__)
	app.config.from_object(os.getenv('APP_SETTINGS'))
	app.secret_key=os.urandom(16)

	from . import models

	models.db.init_app(app)
	migrate.init_app(app, models.db)
	app.register_blueprint(auth.bp)
	app.register_blueprint(projects.bp)
	app.register_blueprint(ideas.bp)

	@app.route('/')
	def index():
		if 'user_id' in session:
			projects=models.Project.query.filter((models.Project.user_id==session['user_id'] and models.Project.is_completed==0)).all()
			return render_template('auth_index.html', projects=projects);

		return render_template('index.html')

	return app

