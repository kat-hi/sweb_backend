import logging

from flask_login import UserMixin
import sweb_backend


class Plantlist(sweb_backend.DB.Model):
	__tablename__ = 'pflanzliste'
	__table_args__ = {'keep_existing': True}
	BaumNr = sweb_backend.DB.Column(sweb_backend.DB.Integer, primary_key=True)
	Pflanzreihe = sweb_backend.DB.Column(sweb_backend.DB.Integer)
	PflanzreihePosition = sweb_backend.DB.Column(sweb_backend.DB.Integer)
	BaumID = sweb_backend.DB.Column(sweb_backend.DB.Integer)
	BaumsortenID = sweb_backend.DB.Column(sweb_backend.DB.Integer)
	FruchtID = sweb_backend.DB.Column(sweb_backend.DB.Integer)
	Frucht = sweb_backend.DB.Column(sweb_backend.DB.String)
	SortenID = sweb_backend.DB.Column(sweb_backend.DB.Integer)
	Sortenzaehler = sweb_backend.DB.Column(sweb_backend.DB.Integer)
	Sorte = sweb_backend.DB.Column(sweb_backend.DB.String)
	Ernte = sweb_backend.DB.Column(sweb_backend.DB.Float)
	PatenID = sweb_backend.DB.Column(sweb_backend.DB.String)
	Longitude = sweb_backend.DB.Column(sweb_backend.DB.Float)
	Latitude = sweb_backend.DB.Column(sweb_backend.DB.Float)


class Sorts(sweb_backend.DB.Model):
	__tablename__ = 'obstsorten'
	__table_args__ = {'keep_existing': True}
	id = sweb_backend.DB.Column(sweb_backend.DB.Integer, primary_key=True)
	fruchtID = sweb_backend.DB.Column(sweb_backend.DB.Integer)
	frucht = sweb_backend.DB.Column(sweb_backend.DB.String)
	sorte = sweb_backend.DB.Column(sweb_backend.DB.String)
	andereNamen = sweb_backend.DB.Column(sweb_backend.DB.String)
	herkunft = sweb_backend.DB.Column(sweb_backend.DB.String)
	groesse = sweb_backend.DB.Column(sweb_backend.DB.String)
	beschreibung = sweb_backend.DB.Column(sweb_backend.DB.String)
	reifezeit = sweb_backend.DB.Column(sweb_backend.DB.String)
	geschmack = sweb_backend.DB.Column(sweb_backend.DB.String)
	verwendung = sweb_backend.DB.Column(sweb_backend.DB.String)
	lager = sweb_backend.DB.Column(sweb_backend.DB.String)
	verbreitung = sweb_backend.DB.Column(sweb_backend.DB.String)


# class Admins(sweb_backend.DB.Model, UserMixin):
# 	__tablename__ = 'admins'
# 	# __table_args__ = {'keep_existing': True}
# 	id = sweb_backend.DB.Column(sweb_backend.DB.String, primary_key=False)
# 	email = sweb_backend.DB.Column(sweb_backend.DB.String, primary_key=True)
# 	authenticated = sweb_backend.DB.Column(sweb_backend.DB.String, default="false")
# 	active = sweb_backend.DB.Column(sweb_backend.DB.String, default="true")
#
# 	def __repr__(self):
# 		return f'{self.id}: Email: {self.email}, authenticated: {self.authenticated}, active: {self.active}'

class User(UserMixin):
	def __init__(self, id_, email):
		self.id = id_
		self.email = email

	@staticmethod
	def get_by_email(user_email):
		logging.info("Get User by email")

		from sweb_backend import DB
		user = DB.session.execute('SELECT * FROM admins WHERE email = :val', {'val': user_email}).fetchone()

		if not user:
			logging.info("--- No user found in get()")
			return None

		logging.info(f"return user {user}")
		return user

	@staticmethod
	def get(id):
		logging.info("Get User by ID")

		from sweb_backend import DB
		user = DB.session.execute('SELECT * FROM admins WHERE id = :val', {'val': id}).fetchone()

		if not user:
			logging.info("--- No user found in get()")
			return None

		logging.info(f"return user {user}")
		return user

	@staticmethod
	def create(id_, email):
		logging.info("Create User")
		from sweb_backend import DB
		DB.session.execute(
			"INSERT INTO admins (id, email) "
			"VALUES (:id, :email)",
			{'id': id_, 'email': email},
		)
		DB.commit()


class Image(sweb_backend.DB.Model):
	__tablename__ = 'Bilder'
	__table_args__ = {'keep_existing': True}
	id = sweb_backend.DB.Column(sweb_backend.DB.Integer, primary_key=True)
	uri = sweb_backend.DB.Column(sweb_backend.DB.String)


def is_active(self):
	"""True, as all users are active."""
	logging.info('IS ACTIVE ' + str(self.active))
	if self.active == "true":
		return True


def get_id(self):
	"""Return the email address to satisfy Flask-Login's requirements."""
	logging.info('GET ID ' + str(self.email))
	return self.email


def is_authenticated(self):
	"""Return True if the user is authenticated."""
	logging.info('IS AUTHENTICATED' + str(self.authenticated))
	if self.authenticated == "true":
		return True


def is_anonymous(self):
	"""False, as anonymous users aren't supported."""
	return False
