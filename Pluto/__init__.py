import os
from flask import Flask, render_template
from . import auth

def create_app(test_config=None):
	app=Flask(__name__, instance_relative_config=True)

	app.config.from_mapping(SECRET_KEY='dev')
	app.register_blueprint(auth.bp)

	@app.route('/')
	def index():
		return render_template('index.html')

	return app

