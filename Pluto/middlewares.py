import functools
from flask import session, redirect, url_for, flash

def guestMiddleware(view):
	@functools.wraps(view)
	def middleware(**kwargs):
		if 'user_id' in session:
			flash('You do not have access', 'info')
			return redirect(url_for('index'))

		return view(**kwargs)

	return middleware


def authMiddleware(view):
	@functools.wraps(view)
	def middleware(**kwargs):
		if 'user_id' not in session:
			flash('You must be logged in', 'error')
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return middleware
