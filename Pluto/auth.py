from flask import render_template, Blueprint, request

bp=Blueprint('auth', __name__)

@bp.route('/signup', methods=('GET', 'POST'))
def signup():
	if request.method == 'POST':
		print('leke')

	return render_template('auth/signup.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		print('leke')

	return render_template('auth/login.html')