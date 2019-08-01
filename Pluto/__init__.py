import os
from flask import Flask, render_template
from flask_migrate import Migrate
from . import auth

migrate=Migrate()

def create_app(test_config=None):
	app=Flask(__name__)
	app.config.from_object(os.getenv('APP_SETTINGS'))

	from . import models

	models.db.init_app(app)
	migrate.init_app(app, models.db)
	app.register_blueprint(auth.bp)

	@app.route('/')
	def index():
		return render_template('index.html')

	return app

