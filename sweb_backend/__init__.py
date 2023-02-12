import os
from pathlib import Path

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask import Flask
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from flask_cors import CORS
from sqlalchemy.exc import OperationalError
from flask_bootstrap import Bootstrap5
from sweb_backend.error_handler import server_error, not_found, not_authorized
import logging

default_log_dir = Path('/app/')
if default_log_dir.exists():
	os.makedirs(os.path.join(default_log_dir, 'log'), exist_ok=True)
	filename = os.path.join(default_log_dir, 'log', 'sweb.log')
else:
	base_dir = os.path.dirname(os.path.dirname(__file__))
	os.makedirs(os.path.join(base_dir, 'log'), exist_ok=True)
	filename = os.path.join(base_dir, 'log', 'sweb.log')

logging.basicConfig(filename=filename, level=logging.DEBUG, format='%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

DB = SQLAlchemy()
MA = Marshmallow()
AD = Admin()
bootstrap = Bootstrap5()
login_manager = LoginManager()


def create_app():
	from sweb_backend.login import admin_login
	from sweb_backend.api import api

	app = Flask(__name__)
	app.logger.root.setLevel(logging.DEBUG)

	with app.app_context():
		set_config_settings(app)
		app.config['CORS_HEADERS'] = 'Content-Type'
		CORS(app, resources={r"/*": {"origins": "*"}})

		bootstrap.init_app(app)
		init_extensions(app)
		register_error_handlers(api, admin_login)
		app.register_blueprint(admin_login)
		login_manager.init_app(app)
		app.register_blueprint(api)
		DB.create_all()

		try:
			init_admin_views()
		except OperationalError as e:
			logging.info(e.orig.args[1])
	return app


def register_error_handlers(api, admin_login):
	api.register_error_handler(404, not_found)
	api.register_error_handler(401, not_authorized)
	api.register_error_handler(500, server_error)
	admin_login.register_error_handler(404, not_found)
	admin_login.register_error_handler(401, not_authorized)


def set_config_settings(app):
	from sweb_backend.config import Config, Production
	app.config['FLASK_ADMIN_SWATCH'] = 'spacelab'
	if os.environ.get('FLASK_DEBUG') == 0:
		app.logger.info('Use development DB.')
		app.config.from_object(Config())
	else:
		app.config.from_object(Production())
		app.logger.info('Use production DB.')
		app.secret_key = Config.SECRETS['SECRET_KEY']

	app.config["FLASK_RUN_PORT"] = app.config.get("FLASK_RUN_PORT")


def init_admin_views():
	from sweb_backend import models, admin_views
	AD.add_view(admin_views.imagetable(models.Image, DB.session))
	AD.add_view(admin_views.pflanzlistetable(models.Plantlist, DB.session))
	AD.add_view(admin_views.obstsortentable(models.Sorts, DB.session))


def init_extensions(app):
	DB.init_app(app)
	MA.init_app(app)
	AD.init_app(app)


try:
	app = create_app()

	limiter = Limiter(
		app=app,
		key_func=get_remote_address,
		default_limits=['300 per hour', '1000 per day']
	)

except Exception as e:
	logging.error(e)
	raise
