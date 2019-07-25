import os
from flask import Flask, render_template

def create_app(test_config=None):
	app=Flask(__name__, instance_relative_config=True)

	app.config.from_mapping(SECRET_KEY='dev')

	@app.route('/')
	def index():
		return render_template('index.html')

	return app