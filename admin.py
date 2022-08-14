from flask import Markup, url_for
from app import app
import os.path as op
from models import db, ProductModels, ProductTags, Products, ProductCategories, \
    ProductCharacteristics, ProductCharacteristicsType, Ingredients, Company
from flask_admin import Admin, AdminIndexView, form
from flask_admin.contrib.sqla import ModelView


# 'base_path': op.join(op.dirname(__file__),
#                                  app.config['MEDIA_FOLDER']),

def _show_img(view, context, model, name):
    if model.img_path:
        filename = f"media/{model.img_path}"
        src = url_for('static',
                      filename=filename)
        markupstring = f"<img src='{src}'/>"
        return Markup(markupstring)
    else:
        return ""


class ProductModelsView(ModelView):
    column_searchable_list = ['name']
    column_labels = {
        'name': 'Название',
        'category': 'Категория',
        'ingredients': 'Ингредиенты',
        'img_path': 'Превью',
        'products': 'Продукты',
        'metric': 'Ед. измерения',
        'labels': 'Лейблы',
        'products': 'Продукты',
    }
    column_formatters = {
        'img_path': _show_img
    }
    form_overrides = {
        'img_path': form.FileUploadField
    }
    form_args = {
        'img_path': {
            'base_path': op.join(op.dirname(__file__),
                                 app.config['MEDIA_FOLDER']),
            'allow_overwrite': True
        }
    }
    column_list = ('name', 'category', 'ingredients', 'img_path', 'products')
    form_columns = ('category', 'name', 'ingredients', 'metric', 'img_path',
                    'tags', 'labels', 'products')

    def create_model(self, form):
        try:
            company = Company.query.first()
            model = self.model()
            model.company_id = company.id
            form.populate_obj(model)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            print('='*80)
            print(ex)
            # if not self.handle_view_exception(ex):
            #     flash(gettext('Failed to create record. %(error)s',
            #                   error=str(ex)), 'error')
            #     log.exception('Failed to create record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model


class ProductTagsView(ModelView):
    column_searchable_list = ['name']
    column_list = ('name', 'product_models')
    column_labels = {
        'name': 'Название',
        'product_models': 'Модель продукта',
    }
    form_columns = ('name', 'product_models')


class ProductsView(ModelView):
    column_searchable_list = ['name']
    column_list = ('name', 'price', 'characteristics', 'additional_products')
    column_labels = {
        'name': 'Название',
        'price': 'Цена',
        'weight': 'Порция (Вес, литры и т.д.)',
        'product_models': 'Модель продукта',
        'characteristics': 'Характеристики',
        'additional_products': 'Доп товары',
    }
    form_columns = ('product_models', 'characteristics', 'name', 'price',
                    'weight', 'additional_products')


class ProductCategoriesView(ModelView):
    column_searchable_list = ['name']
    column_labels = {
        'name': 'Название',
    }
    form_args = {
        'name': {
            'label': 'Название'
        },
    }


class ProductCharacteristicsView(ModelView):
    column_searchable_list = ['name']
    column_labels = {
        'name': 'Название',
    }
    form_args = {
        'name': {
            'label': 'Название'
        },
    }


class ProductCharacteristicTypesView(ModelView):
    column_searchable_list = ['name']
    column_labels = {
        'name': 'Название',
    }
    form_args = {
        'name': {
            'label': 'Название'
        },
    }


class CompanyView(ModelView):
    column_searchable_list = ['title']
    column_labels = {
        'title': 'Название компании',
        'work_start_time': 'Время открытия',
        'work_finish_time': 'Время закрытия',
    }
    form_args = {
        'title': {
            'label': 'Название компании'
        },
        'work_start_time': {
            'label': 'Время открытия'
        },
        'work_finish_time': {
            'label': 'Время закрытия'
        },
    }
    form_columns = ('title', 'work_start_time', 'work_finish_time')


class IngredientsView(ModelView):
    column_searchable_list = ['name']
    column_labels = {
        'name': 'Название',
    }
    form_args = {
        'name': {
            'label': 'Название'
        },
    }


class ProductCategoriesView(ModelView):
    column_searchable_list = ['name']
    column_labels = {
        'name': 'Название',
    }
    form_args = {
        'name': {
            'label': 'Название'
        },
    }

    def get_query(self):
        return self.session.query(self.model).filter(self.model.id == 1)


class AdminMixin:
    pass


class AdminView(AdminMixin, ModelView):
    pass


class HomeView(AdminMixin, AdminIndexView):
    pass


admin = Admin(app, 'Куда пицца', url="/", index_view=HomeView(name="Главная"))
admin.add_view(ProductModelsView(ProductModels, db.session, category="Продукты",
                                 endpoint="/product_models_",
                                 name="Модели продуктов"))
admin.add_view(ProductsView(Products, db.session, endpoint="/products_",
                            category="Продукты", name="Продукты"))
admin.add_view(ProductTagsView(ProductTags, db.session, endpoint="/tags_",
                               name="Теги"))
admin.add_view(ProductCategoriesView(ProductCategories, db.session,
                                     endpoint="/product_categories_",
                                     name="Категории"))
admin.add_view(IngredientsView(Ingredients, db.session, endpoint="/ingredients_",
                               name="Ингредиенты"))
admin.add_view(ProductCharacteristicsView(ProductCharacteristics, db.session,
                                          endpoint="/product_characteristics_",
                                          name="Характеристики",
                                          category="Характеристики"))
admin.add_view(ProductCharacteristicTypesView(ProductCharacteristicsType,
                                              db.session,
                                              endpoint="/product_characteristic_types_",
                                              name="Типы характеристик",
                                              category="Характеристики"))
admin.add_view(CompanyView(Company, db.session, endpoint="/company_",
                           name="Компания"))

