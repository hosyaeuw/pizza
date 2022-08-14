from app import app
import admin

import products
import geocode
import autocomplete
import company

app.register_blueprint(products.products, url_prefix='/api')
app.register_blueprint(geocode.geocode, url_prefix='/api')
app.register_blueprint(autocomplete.autocomplete, url_prefix='/api')
app.register_blueprint(company.company, url_prefix='/api')


if __name__ == '__main__':
    app.run()
