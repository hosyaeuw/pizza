from flask import Blueprint
from flask_restful import Api, Resource
import requests

geocode = Blueprint('geocode', __name__)
api = Api(geocode)


class Geocode(Resource):
    def get(self):
        pass


api.add_resource(Geocode, '/geocode/')
