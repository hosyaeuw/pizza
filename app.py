from flask import Flask, render_template, redirect, jsonify
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


from flask_jwt_extended import JWTManager, jwt_required, verify_jwt_in_request

app = Flask(__name__)
app.config.from_object(Configuration)
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/", defaults={"_path"})
@app.route("/<path:u_path>")
def index(u_path):
    return render_template("index.html")

configApi = {
            "getAddresses": "/v1/user-address/list",
            "createAddress": "/v2/user-addresses",
            "updateAddress": "/v2/user-addresses/${addressId}",
            "deleteAddress": "/v1/user-address/delete",
            "createAnonymousAddress": "/v2/guest-addresses",
            "filterAddresses": "/v2/filtered-addresses",
            "requestEmailAuth": "/v2/auth-email",
            "loginByEmail": "/v2/auth-email/login",
            "registerByEmail": "/v2/auth-email/signup",
            "login": "/v1/auth/login/",
            "loginByService": "/v3/auth/login/",
            "signup": "/v1/auth/signup/",
            "logout": "/v1/auth/logout",
            "update": "/v1/auth/update",
            "recoveryPassword": "/v1/auth/remind-password",
            "requestValidationCode": "/v2/auth-sms/send-code",
            "loginByPhone": "/v2/auth-sms/login",
            "category": "/v1/category/all-with-products?date={date}&paymentType={paymentType}&cityId={cityId}",
            "order": "/v1/order/create",
            "createOrder": "/v2/order/create",
            "history": "/v1/order/history?page={page}&count={count}",
            "promotions": "/v2/promotional-category/products",
            "widget": "/v1/product-set/list",
            "about": "/v1/company/about",
            "feedback": "/v2/feedback/create",
            "setDeviceId": "/v1/profile/set-device",
            "setGuestDeviceId": "/v1/guest/set-device",
            "getProfile": "/v1/profile/get?expand=address",
            "getPeriods": "/v1/shipping-interval/list",
            "getPaymentTypes": "/v1/payment-type/list",
            "orderFeedback": "/v1/order/feedback",
            "cancelOrder": "/v2/order/cancel",
            "orderCancelReasons": "/v1/order-cancel-reason/list",
            "calculate": "/v2/cart/calculate",
            "getPrice": "/v2/product-prices",
            "getInterval": "/v4/shipping-interval/list",
            "getCalendarInterval": "/v3/shipping-interval/list",
            "getCoinsHistory": "/v1/loyalty-system/history",
            "support": "/v1/feedback/support",
            "getChatMessages": "/v3/chat/get-messages",
            "addChatMessage": "/v1/chat/add-message",
            "getAvailableInvite": "/v1/auth/before-signup",
            "getOrder": "/v1/order/get/{orderUUID}",
            "clearPaymentStatus": "/v2/payment/clear-fail",
            "rateApp": "/v1/feedback/rating",
            "getOffices": "/v1/office/list",
            "resetPassword": "/v3/user/reset-password",
            "partnerBillingSystemIpAddress": "1/marketing/create-request-from-app",
            "reverseGeocoding": "/v1/geocoding/reverse",
            "getAddresses": "/v1/user-address/list",
            "createAddress": "/v1/user-address/create",
            "deleteAddress": "/v1/user-address/delete",
        }


@app.route("/requests/")
def req():
    data = {
        "api": configApi,
        "localConfig": {
            "appName": "Aqua Developer",
            "desctiptionApp": "Для разработчиков",
            "mainDomain": "https://aqua-delivery.ru",
            "domain": "https://api.aqua-delivery.ru",
            "oneSignalKey": "01caddeb-d7d6-43c8-bc34-72f8a7597bc2",
            "disabledPhone": True,
            "shareParams": {
                "disabledShare": False,
                "title": "Aqua Developer",
                "message": "Установи приложение и начни заказывать воду удобно без звонков!",
                "link": "http://aqua-delivery.ru",
            },
            "deeplinkHost": "aquadelivery-dev",
            "services": {
                "auth": {
                    "domain": "https://auth.dev.service.appsol.ru",
                    "graphql": "/auth/graphql",
                    "refreshTokenUrl": "/auth/login/token/refresh",
                    "getToken": "/auth/login/token/get",
                    "registration": "/auth/aggregator_users",
                    "resetPasswordRequest": "/auth/reset_password_requests",
                    "confirmSms": "/auth/reset_password_token_requests",
                    "confirmLogin": "/auth/auth_token_requests",
                    "requestAuthCode": "/auth/auth_requests",
                    "completeRegistration": "/auth/complete_registration_requests",
                    "getUserToken": "/auth/anon_token_requests",
                },
                "partner": {
                    "domain": "https://partner.dev.service.appsol.ru",
                    "graphql": "/partner/graphql",
                    "attachUser": "/partner/aggregator_users",
                    "getPartnerToken": "/partner/client_token_requests",
                    "enrichToken": "/partner/enrich_token_requests",
                },
                "payment": {
                    "domain": "https://payment.dev.service.appsol.ru",
                    "graphql": "/payment/graphql",
                    "getPaymentMethods": "/payment/payment_methods",
                    "paymentRequest": "/payment/payment_requests",
                },
                "appVersionChecker": {
                    "domain": "http://app-version-checker.dev.service.appsol.ru",
                    "graphql": "/app-version-checker/graphql",
                    "getVersion": "/app-version-checker/get-app-version",
                },
                "crashReport": {
                    "domain": "https://crash-report.service.appsol.ru",
                    "graphql": "/crash-report/graphql",
                },
                "client": {
                    "domain": "https://client.dev.service.appsol.ru",
                    "graphql": "/client/graphql",
                    "getUserToken": "/client/client_token_requests",
                },
                "user": {
                    "domain": "https://user.dev.service.appsol.ru",
                    "graphql": "/user/graphql",
                    "userLocations": "/user/users/{userId}/locations",
                },
                "logger": {
                    "domain": "https://logger.service.appsol.ru",
                    "graphql": "/logger/graphql",
                    "createLog": "/logger/create-log",
                },
                "marketing": {
                    "domain": "https://marketing.dev.service.appsol.ru",
                    "graphql": "/marketing/graphql",
                    "enrichToken": "https://partner.dev.service.appsol.ru/partner/enrich_token_requests",
                },
            },
            "aggregatorToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2MDk4NTE2MDAsInJvbGVzIjpbIkFOT05ZTU9VU19BR0dSRUdBVE9SX0NMSUVOVCJdLCJ1c2VybmFtZSI6IiIsImV4cCI6MzE4NzY4ODQwMCwiYWdncmVnYXRvciI6ImI1NmYxNWM4LTA5ODYtNDg2ZC1iMGU0LTRmMTYyMWY3NTNhMiIsInV1aWQiOiJkMGIyZWU0Yy0xYmJmLTRhY2EtOTI4MS1lNjQxMTMzYjIzNjEiLCJwaG9uZSI6bnVsbCwiZmlyc3RfbmFtZSI6bnVsbCwibWlkZGxlX25hbWUiOm51bGwsImZhbWlseV9uYW1lIjpudWxsfQ.eg18tKZIxAbUU-vCPY_M1yYGJPhR5I4WLkvFllONa9rwYZWireK5KL1vDsoorJ0d5bXDOn4X63tCpRXCDVXooE2ANz7NMz1Ue_mv0hCWtA8KepHJmkANKhM0MI_0z1KScwI0QdJOSezm6tltxdrXdJKDcCCtZuSyRoePyot6mdp1gpbRLLUo7_kulAxea2nDWuhwcIGyFRaeFm6h0cV-0nBtZcXja1uRirKkkrVKlaAOWcN1N-95mFK2WCHDeDoDoErCLY02ILBps7DxricnbqIFqmVZ9V4bJe5Evsu1ZFhmrJU73A1jAW8A1UwXxwhrQqPNjoBHgo3cvVSnRBaSw7_8sWbLVA6qHfgS6fNaYNadNEtDZ4BCsK1ceTqJK8yeligXWs5ojh8pBghox70ZlcwjkfwOFTvrv72i6AWXwkHTJEmTZwIDexKutYka6PuS_kp2b4Shy3Cgvi9_ml3YRYFS9WpxW36g1pyNwDm5b9fz9nXMY8H8Qwhl961QKnhzZHkTrP41rVhhusx45mgvuKpb6j-yqb51C0UpL_3P6Xjp9RixWxojwLBEonndM9p9psAh5iXwfzHCk-3Rain0hUQHaijbVHmTxAZWjULmBR8GdSxXJPJnsk-6isCSpSE_AXZNb7IpHkalbPjzPmOr1IfR0_6H6_HykPtYv82nDBk",
            "appleAppId": "1446763988",
            "appMetricaKey": "8330eb48-48d2-4d3f-bf8e-5301dd424768",
            "mainDomain": "ttps://aqua-delivery.ru",
            "domain": "ttps://api.aqua-delivery.ru",
            "api": configApi,
            "pushActions": {
                "goTo": "oTo",
                "execute": "xecute"
            },
            "oneSignalKey": "1caddeb-d7d6-43c8-bc34-72f8a7597bc2",
            "googleMapApiToken": "IzaSyBY4H1x6e93nx37ATDnjcdLqkkRWB2ybqI",
            "appMetricaConfig": {
                "apiKey": "8330eb48-48d2-4d3f-bf8e-5301dd424768",
                "crashReporting": False,
                "sessionTimeout": 120,
            },
            "mapboxKey": "k.eyJ1IjoiYXF1YWRlbGl2ZXJ5IiwiYSI6ImNrcWpqenRkNDNoZm4zMm12aWRpdm5uOHQifQ.ien34AQ44w_g6cA27m_IcA"
        },
    }
    return jsonify(data)


# JWT
jwt = JWTManager(app)
#
# # ADMIN
# from models import Colors, Widgets, Transactions, Categories
# from flask_admin import Admin, AdminIndexView
# from flask_admin.contrib.sqla import ModelView
#
#
# class AdminMixin:
# 	def is_accessible(self, **kwargs):
# 		print(self._template_args)
# 		return True
#
# 	def inaccessible_callback(self, name):
# 		return redirect("/auth", code=302)
#
#
# class AdminView(AdminMixin, ModelView):
# 	pass
#
#
# class HomeView(AdminMixin, AdminIndexView):
# 	pass
#
#
# admin = Admin(app, "ockets" url="/", index_view=HomeView(name="Home"))
# admin.add_view(AdminView(Colors, db.session))
# admin.add_view(AdminView(Widgets, db.session, endpoint="widgets_"))
# admin.add_view(AdminView(Transactions, db.session, endpoint="transactions_"))
# admin.add_view(AdminView(Categories, db.session, endpoint="categories_"))
