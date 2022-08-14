from app import db
from datetime import datetime
from utils.timeHelper import DateHelper


ProductTags_ProductModels = db.Table('productTags_productModels',
                                     db.Column('product_tag_id',
                                               db.Integer,
                                               db.ForeignKey('product_tags.id')),
                                     db.Column('product_model_id',
                                               db.Integer,
                                               db.ForeignKey('product_models.id'))
                                     )

ProductModels_Ingredients = db.Table('productModels_ingredients',
                                     db.Column('product_model_id',
                                               db.Integer,
                                               db.ForeignKey('product_models.id')),
                                     db.Column('ingredient_id',
                                               db.Integer,
                                               db.ForeignKey('ingredients.id'))
                                     )

ProductCharacteristics_Products = db.Table('productCharacteristics_products',
                                           db.Column('product_characteristic_id',
                                                     db.Integer,
                                                     db.ForeignKey('product_characteristics.id')),
                                           db.Column('products_id',
                                                     db.Integer,
                                                     db.ForeignKey('products.id'))
                                           )

AdditionalProducts = db.Table('additionalProducts',
                              db.Column('parent_product_id', db.Integer,
                                        db.ForeignKey('products.id')),
                              db.Column('child_product_id', db.Integer,
                                        db.ForeignKey('products.id'))
                              )

ProductModels_Labels = db.Table('productModels_label',
                                db.Column('product_model_id',
                                          db.Integer,
                                          db.ForeignKey('product_models.id')),
                                db.Column('ingredient_id',
                                          db.Integer,
                                          db.ForeignKey('product_model_labels.id'))
                                )


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    work_start_time = db.Column(db.Time(), nullable=False)
    work_finish_time = db.Column(db.Time(), nullable=False)
    logo_path = db.Column(db.String(255))
    # logo_path = db.Column(db.String(255), nullable=False)
    promotions = db.relationship('Promotions',
                                 backref=db.backref('company',
                                                    lazy=True))

    users = db.relationship('Users',
                            backref=db.backref('company', lazy=True))

    product_models = db.relationship('ProductModels',
                                     backref=db.backref('company',
                                                        lazy=True))

    def __init__(self, **kwargs):
        super(Company, self).__init__(**kwargs)


class Promotions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    preview = db.Column(db.String(255), nullable=True)

    company_id = db.Column(db.Integer,
                           db.ForeignKey('company.id',
                                         ondelete="CASCADE"),
                           nullable=False)

    imgs = db.relationship('PromotionImgs',
                           backref=db.backref('promotion', lazy=True))

    def __init__(self, **kwargs):
        super(Promotions, self).__init__(**kwargs)

    def __repr__(self):
        return self.preview


class PromotionImgs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_path = db.Column(db.String(255), nullable=True)

    promotion_id = db.Column(db.Integer,
                             db.ForeignKey('promotions.id',
                                           ondelete="CASCADE"),
                             nullable=False)

    def __init__(self, **kwargs):
        super(PromotionImgs, self).__init__(**kwargs)

    def __repr__(self):
        return self.img_path


class Promocodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.now())
    create_from = db.Column(db.DateTime,
                            default=DateHelper.add_years(datetime.now(), 1))

    company_id = db.Column(db.Integer,
                           db.ForeignKey('company.id',
                                         ondelete="CASCADE"),
                           nullable=False)

    def __init__(self, **kwargs):
        super(Promocodes, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class ProductAdditionalIngredientPrices(db.Model):
    product_id = db.Column(db.Integer,
                           db.ForeignKey('products.id'), primary_key=True)
    ingredient = db.Column(db.Integer,
                           db.ForeignKey('ingredients.id'), primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        super(ProductAdditionalIngredientPrices, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class ProductModelLabels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        super(ProductModelLabels, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class Payments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        super(Payments, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class OrderStatuses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        super(OrderStatuses, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class CartStatuses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    carts = db.relationship('Cart',
                            backref=db.backref('cart_statuses', lazy=True))

    def __init__(self, **kwargs):
        super(CartStatuses, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class ProductCharacteristicsType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    product_characteristics = db.relationship('ProductCharacteristics',
                                              backref=db.backref('product_characteristics_type',
                                                                 lazy=True))

    def __init__(self, **kwargs):
        super(ProductCharacteristicsType, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class ProductCharacteristics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    product_characteristics_type_id = db.Column(db.Integer,
                                                db.ForeignKey('product_characteristics_type.id'),
                                                nullable=False)

    def __init__(self, **kwargs):
        super(ProductCharacteristics, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class ProductCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    img_path = db.Column(db.String(255), nullable=True)
    showInCart = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(ProductCategories, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class MetricSystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    short_name = db.Column(db.String(10), nullable=True)

    ingredients = db.relationship('Ingredients',
                                  backref=db.backref('metric', lazy=True))

    products = db.relationship('ProductModels',
                               backref=db.backref('metric', lazy=True))

    def __init__(self, **kwargs):
        super(MetricSystem, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class ProductTags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        super(ProductTags, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)
    metric_system_id = db.Column(db.Integer,
                                 db.ForeignKey('metric_system.id'),
                                 nullable=False)

    additional_products = db.relationship('ProductAdditionalIngredientPrices',
                                          backref=db.backref('ingredients',
                                                             lazy=True))

    def __init__(self, **kwargs):
        super(Ingredients, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id',
                                      ondelete="NO ACTION"),
                        nullable=False)
    cart_status_id = db.Column(db.Integer,
                               db.ForeignKey('cart_statuses.id',
                                             ondelete="NO ACTION"),
                               nullable=False)

    def __init__(self, **kwargs):
        super(Cart, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer,
                           db.ForeignKey('payments.id', ondelete="NO ACTION"),
                           nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id',
                                      ondelete="NO ACTION"),
                        nullable=False)
    order_status_id = db.Column(db.Integer,
                                db.ForeignKey('order_statuses.id',
                                              ondelete="NO ACTION"),
                                nullable=False)
    card_id = db.Column(db.Integer,
                        db.ForeignKey('cart.id'),
                        nullable=False)
    db.Column(db.DateTime, default=datetime.now())

    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class ProductModels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now())
    img_path = db.Column(db.String(255), nullable=False)

    metric_system_id = db.Column(db.Integer,
                                 db.ForeignKey('metric_system.id'),
                                 nullable=False)

    company_id = db.Column(db.Integer,
                           db.ForeignKey('company.id',
                                         ondelete="CASCADE"),
                           nullable=False)

    category_id = db.Column(db.Integer,
                            db.ForeignKey('product_categories.id',
                                          ondelete="CASCADE"),
                            nullable=False)

    metric_system_id = db.Column(db.Integer,
                                 db.ForeignKey('metric_system.id'),
                                 nullable=False)

    products = db.relationship('Products',
                               backref=db.backref('product_models', lazy=True))

    category = db.relationship('ProductCategories',
                               backref=db.backref('product_models', lazy=True))

    tags = db.relationship('ProductTags', secondary=ProductTags_ProductModels,
                           backref=db.backref('product_models',
                                              lazy="dynamic"))

    ingredients = db.relationship('Ingredients',
                                  secondary=ProductModels_Ingredients,
                                  backref=db.backref('product_models',
                                                     lazy="dynamic"))

    labels = db.relationship('ProductModelLabels',
                             secondary=ProductModels_Labels,
                             backref=db.backref('product_models',
                                                lazy="dynamic"))

    def __init__(self, **kwargs):
        super(ProductModels, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    product_model_id = db.Column(db.Integer,
                                 db.ForeignKey('product_models.id',
                                               ondelete="CASCADE"),
                                 nullable=False)

    additional_ingredients = db.relationship('ProductAdditionalIngredientPrices',
                                             backref=db.backref('products',
                                                                lazy=True))

    characteristics = db.relationship('ProductCharacteristics',
                                      secondary=ProductCharacteristics_Products,
                                      backref=db.backref('products',
                                                         lazy="dynamic"))

    additional_products = db.relationship("Products",
                                          secondary=AdditionalProducts,
                                          primaryjoin=id ==
                                                      AdditionalProducts.c.parent_product_id,
                                          secondaryjoin=id ==
                                                        AdditionalProducts.c.child_product_id,
                                          )

    def __init__(self, **kwargs):
        super(Products, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class CartProducts(db.Model):
    cart_id = db.Column(db.Integer,
                        db.ForeignKey('cart.id',
                                      ondelete="NO ACTION"),
                        nullable=False,
                        primary_key=True)
    product_id = db.Column(db.Integer,
                           db.ForeignKey('products.id',
                                         ondelete="NO ACTION"),
                           nullable=False,
                           primary_key=True)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(CartProducts, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


class IngredientsCartProducts(db.Model):
    cart_id = db.Column(db.Integer,
                        db.ForeignKey('cart.id',
                                      ondelete="NO ACTION"),
                        nullable=False,
                        primary_key=True)
    product_id = db.Column(db.Integer,
                           db.ForeignKey('products.id',
                                         ondelete="NO ACTION"),
                           nullable=False,
                           primary_key=True)
    ingredient_id = db.Column(db.Integer,
                              db.ForeignKey('ingredients.id',
                                            ondelete="NO ACTION"),
                              nullable=False,
                              primary_key=True)
    isAdd = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        super(IngredientsCartProducts, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


# Юзеры
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    house = db.Column(db.String(7), nullable=False)
    entrance = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    apartment_number = db.Column(db.Integer, nullable=False)
    intercom_code = db.Column(db.Integer, nullable=False)
    bonuses = db.Column(db.Integer, default=0)

    company_id = db.Column(db.Integer,
                           db.ForeignKey('company.id',
                                         ondelete="CASCADE"),
                           nullable=False)

    carts = db.relationship('Cart',
                            backref=db.backref('user', lazy=True))

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)

    def __repr__(self):
        return f'{self.phone} {self.name} {self.email}'


class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        super(UserRoles, self).__init__(**kwargs)

    def __repr__(self):
        return self.name


User_UserRoles = db.Table('User_UserRoles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('userRoles_id', db.Integer, db.ForeignKey('user_roles.id'))
)


def create_db():
    db.create_all()
    db.session.commit()

    ms1 = MetricSystem(name="граммы", short_name="г.")
    ms2 = MetricSystem(name="литры", short_name="л.")
    db.session.add_all([ms1, ms2])
    db.session.commit()

    i1 = Ingredients(name="Сыр моцарелла", metric_system_id=ms1.id)
    i2 = Ingredients(name="Томатный соус", metric_system_id=ms2.id)
    db.session.add_all([i1, i2])
    db.session.commit()

    pc1 = ProductCategories(name="Пицца")
    pc2 = ProductCategories(name="Суши")
    pc3 = ProductCategories(name="Напитки")
    db.session.add_all([pc1, pc2, pc3])
    db.session.commit()


def delete_db():
    db.drop_all()
    db.session.commit()


if __name__ == '__main__':
    create_db()
    # delete_db()
    # try:
    #     create_db()
    # except:
    #     delete_db()
    #     create_db()
