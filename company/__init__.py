from flask import Blueprint
from flask_restful import Api, Resource
from models import Company

company = Blueprint('company', __name__)
api = Api(company)


class CompanyAPI(Resource):
    def get(self):
        company = Company.query.first()
        result = {
            'id': company.id,
            'timeStart': company.work_start_time.strftime('%H:%M'),
            'timeFinish': company.work_finish_time.strftime('%H:%M'),
            'averageDeliveryTime': '00:24:19',
        }
        return {
            'success': True,
            'result': result,
        }


api.add_resource(CompanyAPI, '/company/')
