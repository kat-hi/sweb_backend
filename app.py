from sweb_backend import app

if __name__ == "__main__":
	app.run(port=app.config.get('FLASK_RUN_PORT', 5000))
