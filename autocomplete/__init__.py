from flask import Blueprint
from flask_restful import Api, Resource
import requests

autocomplete = Blueprint('autocomplete', __name__)
api = Api(autocomplete)


class Autocomplete(Resource):
    def get(self):
        url = 'https://photon.komoot.io/api/?q='


api.add_resource(Autocomplete, '/autocomplete/')
