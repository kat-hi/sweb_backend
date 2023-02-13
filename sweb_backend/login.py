from flask_login import current_user, login_required, login_user, logout_user
from flask import request, redirect, Blueprint, render_template
from flask import current_app as app

from sweb_backend import login_manager
import requests
import json

admin_login = Blueprint('admin_login', __name__)
CURRENT_EMAIL = str()


@login_manager.user_loader
def load_user(user_id):
	from sweb_backend.models import User
	app.logger.info(f"USER LOADER: {user_id}")
	return User.get(user_id)


# TODO HttpError handling
# getting the provider configuration document
def _get_google_provider_cfg():
	url = app.config.get("LOGIN", {}).get('GOOGLE_DISCOVERY_URL')
	return requests.get(url).json()


# this function is to associate the user_id in the cookie with the actual user object
# user_id is the user_id from the cookies that is created when a user logs in.
def flask_user_authentication(users_email, unique_id):
	from sweb_backend.models import User
	app.logger.info(f'flask_user_authentication: {unique_id}')

	allowed_emails = [app.config.get("LOGIN", {}).get("ADMIN_EMAIL_1"),
					  app.config.get("LOGIN", {}).get("ADMIN_EMAIL_2")]

	if users_email in allowed_emails:
		user = User.get(users_email)
		if not user:
			app.logger.info("NOT USER")
			User.create(unique_id[:8], users_email)
			user = User.get(unique_id[:8])

		app.logger.info(user)
		global CURRENT_EMAIL
		CURRENT_EMAIL = users_email
		login_user(user, remember=True, force=True)
		return True
	else:
		app.logger.info('FLASK USER AUTHENTICATION FAILED')
		return False


@admin_login.route('/')
def root():
	app.logger.info("admin login route /")
	admin_base_url = app.config.get("ADMIN_BASE_URL")
	if 'http://' in str(request.url):
		return redirect('http://' + admin_base_url + '/app/admin')
	elif 'https://' in str(request.url):
		return redirect('https://' + admin_base_url + '/app/admin')


@admin_login.route('/app/admin')
def admin_home():
	app.logger.info("admin home route /app/admin")
	admin_base_url = app.config.get("ADMIN_BASE_URL")
	if current_user.is_authenticated:
		app.logger.info('current user: ' + str(current_user))
		app.logger.info(f'redirect to https://{admin_base_url}/admin')
		return redirect(f'https://{admin_base_url}/admin')
	else:
		return render_template('login.html')


@admin_login.route('/app/admin/login')
def google_login():
	app.logger.info("GOOGLE_LOGIN: /app/admin/login")
	app.logger.info(request.base_url)
	app.logger.info(request.base_url.replace('http://', 'https://') + '/callback')

	# auth-endpoint contains URL to instantiate the OAuth2 flow with Google from this client app
	google_provider_cfg = _get_google_provider_cfg()
	authorization_endpoint = google_provider_cfg['authorization_endpoint']
	# Use library to construct request for Google login + provide scopes that let retrieve user's profile from Google
	client = app.config.get("LOGIN", {}).get("CLIENT")
	request_uri = client.prepare_request_uri(
		authorization_endpoint,
		redirect_uri=request.base_url.replace('http://', 'https://') + '/callback',
		scope=['openid', 'email', 'profile'])
	app.logger.info(request_uri)
	return redirect(request_uri)


@admin_login.route("/app/admin/login/callback")
def callback():
	global USERS_EMAIL
	app.logger.info("CALLBACK /app/admin/login/callback")
	admin_base_url = app.config.get("ADMIN_BASE_URL")

	# Get authorization code Google sent back to you
	code = request.args.get("code")
	google_provider_cfg = _get_google_provider_cfg()
	token_endpoint = google_provider_cfg["token_endpoint"]
	client = app.config.get("LOGIN", {}).get("CLIENT")
	app.logger.info(request.url)
	token_url, headers, body = client.prepare_token_request(
		token_endpoint,
		authorization_response=request.url.replace('http://', 'https://'),
		redirect_url=request.base_url.replace('http://', 'https://'),
		code=code
	)
	app.logger.info('GOT TOKEN_URL from /callback ' + token_url)
	client_id = app.config.get("SECRETS", {}).get("GOOGLE_CLIENT_ID")
	client_secret = app.config.get("SECRETS", {}).get("GOOGLE_CLIENT_SECRET")

	token_response = requests.post(
		token_url,
		headers=headers,
		data=body,
		auth=(client_id, client_secret)
	)
	app.logger.info("TOKEN RESPONSE")

	app.logger.info(token_response)
	client = app.config.get("LOGIN", {}).get("CLIENT")
	client.parse_request_body_response(json.dumps(token_response.json()))
	# find and hit the URL from Google that gives you the user's profile information,
	userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
	uri, headers, body = client.add_token(userinfo_endpoint)
	userinfo_response = requests.get(uri, headers=headers, data=body)

	# verification
	# if userinfo_response.json().get("email_verified"):
	unique_id = userinfo_response.json().get("sub", "")
	user_email = userinfo_response.json().get("email", "")
	users_name = userinfo_response.json().get("given_name", "")
	app.logger.info('GOT USER DATA from /callback: ' + unique_id + ' ' + user_email + ' ' + users_name)

	if flask_user_authentication(user_email, unique_id):
		app.logger.info(f"AUTH SUCCESS REDIRECT TO: {'https://' + admin_base_url + '/admin'}")
		return redirect('https://' + admin_base_url + '/admin')
	else:
		return render_template('401.html')


@admin_login.route("/app/admin/logout")
def logout():
	# from sweb_backend import DB
	app.logger.info("admin home route /app/admin/logout")
	app.logger.info(f'current_user: {current_user}')
	logout_user()
	admin_base_url = app.config.get("ADMIN_BASE_URL")
	return redirect('https://' + admin_base_url)
