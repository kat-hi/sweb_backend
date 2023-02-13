import logging

import requests
import re
from flask import current_app as app
from sweb_backend.config import Config


def extract_values_from_json(response):
	email = str(response['email'])
	lastname = str(response['lastName'])
	streetaddress = str(response['streetAddress'])
	cityaddress = str(response['cityAddress'])
	message = str(response['message'])
	firstname = str(response['firstName'])
	phone = str(response['phone'])
	data = [email, lastname, streetaddress, cityaddress, message, firstname, phone]
	logging.info('extract_values_from_json: ' + str(data))
	return data


def get_valid_image_uri(image_output):
	checked_files = []
	from flask import current_app
	base_download_url = current_app.config.get("IMAGE_BASE_URL")
	imagelist = eval(image_output[0])
	app.logger.info(imagelist)

	for image in imagelist:
		try:
			regex = 'lnk/[\w]*'
			image_id = re.search(regex, image['uri']).group().split('lnk/')[1]
			image_uri = f'{base_download_url}{image_id}'
			app.logger.info(f"check: {image_id}")
			response = requests.head(image_uri)

			app.logger.info(f"RESPONSE: {response}")
			if response.status_code is 200 and (
				response.headers['Content-Type'] == 'image/png' or response.headers['Content-Type'] == 'image/jpeg'):
				app.logger.info('response' + str(response))
				checked_files.append(base_download_url + image_id)
			else:
				app.logger.info(f'image not available: {image}')
		except TypeError as e:
			app.logger.info(f'TypeError: {e}')
	return checked_files
