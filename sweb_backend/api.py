import json
import logging

from flask import jsonify, request, Blueprint
from sweb_backend import dbservice, models, schemas, dataservice
from flask import current_app as app
api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/', methods=['GET'])
def index():
	response = jsonify({'json sagt': 'Hallo i bims. der json.'})
	app.logger.info(f"Hallo I bims")
	return response, 200


@api.route('/karte', methods=['GET'])
def infos():
	app.logger.info("request /karte")
	return dbservice.get_json_data(models.Plantlist, schemas.Tree, id=None)


@api.route('/karte/baeume', methods=['GET'])
def get_trees():
	app.logger.info("request /karte/baeume")
	return dbservice.get_json_data(models.Sorts, schemas.Sorts, id=None)


@api.route('/karte/baeume/<id>', methods=['GET'])
def get_tree(id):
	app.logger.info(f"request /karte/baeume/{id}")
	return dbservice.get_json_data(models.Plantlist, schemas.Tree, id=id)


@api.route('/karte/baeume/koordinaten', methods=['GET'])
def get_coordinates():
	app.logger.info("request /karte/baeume/koordinaten")
	return dbservice.get_json_data(models.Plantlist, schemas.Treecoordinates, id=None)


@api.route('/karte/baeume/<id>/koordinaten', methods=['GET'])
def get_coordinates_of_tree(id):
	app.logger.info(f"request /karte/baeume/{id}/koordinaten")
	return dbservice.get_json_data(models.Plantlist, schemas.Treecoordinates, id=id)


@api.route('/karte/baeume/properties', methods=['GET'])
def get_imagelinks():
	app.logger.info(f"request imagelinks")
	image_output = dbservice.get_json_data(models.Image, schemas.Image, id=None)
	checked_files = dataservice.get_valid_image_uri(image_output)
	app.logger.info(checked_files)
	return jsonify({'data': checked_files}), 200


@api.route('/kontakt', methods=['POST'])
def fetch_contact_information():
	from sweb_backend import mail
	logging.info(json.loads(request.data.decode('utf-8')))
	response = json.loads(request.data.decode('utf-8'))
	try:
		mail.connect_to_smtp_server(response)
	except Exception as e:
		app.logger.info(e)
		return '', 400

	return '', 200
