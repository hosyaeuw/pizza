from flask import Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import get_jwt, jwt_required
from models import ProductModels, ProductCategories, Products, ProductCharacteristics
from utils.files import get_img_url
from utils.text import transliterate_text
from datetime import datetime

products = Blueprint('products', __name__)
api = Api(products)


def get_filter(characteristics_id, type_id, model_id):
    p_ids = Products.query.filter(
        Products.characteristics.any(ProductCharacteristics.id ==
                                     characteristics_id),
        Products.product_model_id == model_id).subquery('p_ids')
    chars = ProductCharacteristics.query.filter(
        ProductCharacteristics.product_characteristics_type_id != type_id,
        ProductCharacteristics.products.any(Products.id == p_ids.c.id)).all()
    return sorted([char.id for char in chars])


def get_selects(product_model):
    chars = []
    for product in product_model.products:
        chars += product.characteristics
    type_ids = []
    char_ids = []
    result = []
    for char in chars:
        if char.product_characteristics_type_id not in type_ids:
            type_ids.append(char.product_characteristics_type_id)
            char_ids.append(char.id)
            result.append({
                'id': char.product_characteristics_type.id,
                'name': char.product_characteristics_type.name,
                'value': transliterate_text(
                    char.product_characteristics_type.name),
                'items': [
                    {
                        'id': char.id,
                        'name': char.name
                    }
                ]
            })
        else:
            if char.id not in char_ids:
                idx = type_ids.index(char.product_characteristics_type_id)
                result[idx]['items'].append({
                        'id': char.id,
                        'name': char.name
                    })
                char_ids.append(char.id)
    return result


class ProductsAPI(Resource):
    def get(self):
        categories = ProductCategories.query.all()
        items = []
        start = datetime.now()
        for category in categories:
            product_models = ProductModels.query.filter(
                ProductModels.category == category).all()
            data_items = [{
                    'id': product_model.id,
                    'name': product_model.name,
                    'photo': get_img_url(product_model.img_path),
                    'selects': get_selects(product_model),
                    'ingredients': [{
                        'id': ingredient.id,
                        'name': ingredient.name,
                        'price': ingredient.price,
                    } for ingredient in
                        product_model.ingredients],
                    'tags': [{
                        'id': tag.id,
                        'name': tag.name,
                    } for tag in product_model.tags],
                    'products': [{
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'photo': get_img_url(product_model.img_path),
                        'weight': {
                            'count': product.weight,
                        },
                        'characteristics': [{
                            'id': characteristic.id,
                            'name': characteristic.name,
                            'filter': get_filter(characteristic.id,
                                                 characteristic.product_characteristics_type.id,
                                                 product_model.id),
                            'type': {
                                'id': characteristic.product_characteristics_type.id,
                                'name': characteristic.product_characteristics_type.name,
                                'value': transliterate_text(characteristic.product_characteristics_type.name)
                            }
                        } for characteristic in product.characteristics],
                        'additional_product': [additional_product.id for
                                               additional_product in
                                               product.additional_products]
                    } for product in product_model.products]
                } for product_model in product_models]
            if len(data_items) > 0:
                data = {
                    'category': {
                        'id': category.id,
                        'name': category.name
                    },
                    'product_models': data_items
                }
                items.append(data)
        return {
            'success': True,
            'result': items
        }

    def post(self):
        pass


class ProductAPI(Resource):
    def put(self):
        pass

    def delete(self):
        pass


api.add_resource(ProductsAPI, '/products/')
api.add_resource(ProductAPI, '/products/<id>/')
