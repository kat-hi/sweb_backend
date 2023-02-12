import json
import os
from pathlib import Path

from oauthlib.oauth2 import WebApplicationClient

base_dir = os.path.dirname(os.path.dirname(__file__))
config_path = Path(base_dir, 'config.json')


class Config():
	if config_path.exists():
		with open(config_path, 'r') as fp:
			config = json.load(fp)
	else:
		raise SystemExit(f"Please provide a config file here: {config_path}")

	FLASK_RUN_PORT = config.get("FLASK_RUN_PORT", 5000)
	FLASK_APP = config.get("FLASK_APP")

	SECRETS = {
		'GOOGLE_CLIENT_ID': config.get('GOOGLE_CLIENT_ID', None),
		'GOOGLE_CLIENT_SECRET': config.get('GOOGLE_CLIENT_SECRET', None),
		'SECRET_KEY': config.get("SECRET_KEY"),
	}

	EMAIL = {
		"SMTP_PORT": config.get("SMTP_PORT"),
		"SMTP_SERVER": config.get("SMTP_SERVER"),
		"RECEIVER_EMAIL": config.get("RECEIVER_EMAIL"),
		"SENDER_EMAIL": config.get("SENDER_EMAIL"),
		"SMTP_PASSWORD": config.get("SMTP_PASSWORD"),
	}

	LOGIN = {
		'ADMIN_EMAIL_1': config.get('ADMIN_EMAIL_1', ''),
		'ADMIN_EMAIL_2': config.get('ADMIN_EMAIL_2', ''),
		'CLIENT': WebApplicationClient(SECRETS.get('GOOGLE_CLIENT_ID', '')),
		'GOOGLE_DISCOVERY_URL': 'https://accounts.google.com/.well-known/openid-configuration'
	}

	SMTP = {
		'PORT': config.get('SMTP_PORT', ''),
		'SERVER': config.get('SMTP_SERVER', ''),
		'SENDER': config.get('SENDER_EMAIL', ''),
		'RECEIVER': config.get('RECEIVER_EMAIL', ''),
		'PASSWORD': config.get('SMTP_PASSWORD', '')
	}

	IMAGE_BASE_URL = config.get('IMAGE_BASE_URL', '')
	ADMIN_BASE_URL = config.get('ADMIN_BASE_URL', '')


class Production(Config):
	if config_path.exists():
		with open(config_path, 'r') as fp:
			config = json.load(fp)
	else:
		raise SystemExit(f"Please provide a config file here: {config_path}")

	DATABASE = {
		'HOST': config.get('MYSQL_ROOT_HOST', ''),
		'USER': config.get('MYSQL_USER', ''),
		'PASSWORD': config.get('MYSQL_PASSWORD', ''),
		'DBNAME': config.get('MYSQL_DATABASE', ''),
		'PORT': config.get('MYSQL_PORT')
	}
	LOG_DIR = config.get("LOG_DIR")

	IMAGE_BASE_URL = config.get("IMAGE_BASE_URL")

	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DATABASE['USER'] + ':' + DATABASE['PASSWORD'] + '@' \
							  + DATABASE['HOST'] + ':' + DATABASE['PORT'] + '/' + DATABASE['DBNAME']
