import smtplib, ssl
from _socket import gaierror
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app as app

PORT = app.config.get("SMTP", {}).get("PORT")
SENDER = app.config.get("SMTP", {}).get("SENDER")
SERVER = app.config.get("SMTP", {}).get("SERVER")
RECEIVER = app.config.get("SMTP", {}).get("RECEIVER")
PASSWORD = app.config.get("SMTP", {}).get("PASSWORD")


def _plain_text_mail(data):
	return 'Absender:\n' + data['firstName'] + ' ' + data['lastName'] + '\n' \
		+ data['streetAddress'] + '\n' + data['cityAddress'] + '\n' + data['email'] + '\n' \
		+ 'Tel: ' + data['phone'] + '\n\n' + 'Nachricht:\n' + data['message']


def connect_to_smtp_server(datalist):
	app.logger.info('LOGINTO: ' + str(datalist))
	message = MIMEMultipart("alternative")
	message["Subject"] = "Anfrage: Baumpatenschaft"
	message["From"] = datalist['email']
	message["To"] = RECEIVER
	part1 = MIMEText(_plain_text_mail(datalist), "plain")
	message.attach(part1)
	app.logger.info(f'sender {SENDER}')
	app.logger.info(f'receiver {RECEIVER}')
	app.logger.info(f'port {PORT}')
	app.logger.info(f'pass {PASSWORD}')
	app.logger.info(f'server {SERVER}')

	try:
		with smtplib.SMTP(host=SERVER, port=int(PORT)) as server:
			server.ehlo()
			server.starttls()
			server.login(SENDER, PASSWORD)
			server.sendmail(SENDER, RECEIVER, message.as_string())
			server.quit()
	except (gaierror, ConnectionRefusedError) as e:
		app.logger.info(f'Failed to connect to the server. Bad connection settings? {e}')
		raise
	except smtplib.SMTPServerDisconnected as e:
		app.logger.info(f'Failed to connect to the server. Wrong user/password? {e}')
		raise
	except smtplib.SMTPException as e:
		app.logger.info('SMTP error occurred: ' + str(e))
		raise
	except TimeoutError as e:
		app.logger.info(f'Connection time out! {e}')
		raise

	app.logger.info('Sent')
