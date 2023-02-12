from flask import render_template


def server_error(e):
	return render_template('500.html'), 500


def not_found(e):
	return render_template('404.html'), 404


def not_authorized(e):
	return render_template('401.html'), 401
