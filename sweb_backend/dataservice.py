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
	app.logger.info(f'get valid image uri: {base_download_url}')
	imagelist = eval(image_output[0])
	app.logger.info(imagelist)

	for image in imagelist:
		try:
			regex = 'lnk/[\w]*'
			image_id = re.search(regex, image['uri']).group().split('lnk/')[1]
			response = requests.head(base_download_url + image_id)
			app.logger.info(f"RESPONSE: {response}")
			if response.status_code is 200 and (
				response.headers['Content-Type'] == 'image/png' or response.headers['Content-Type'] == 'image/jpeg'):
				app.logger.info('get_valid_image_uri ' + str(response))
				checked_files.append(base_download_url + image_id)
			else:
				app.logger.info('image not available: {}'.format(image))
		except TypeError as e:
			app.logger.info('TypeError: {}'.format(e))
	return checked_files
