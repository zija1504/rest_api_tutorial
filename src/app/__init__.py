from flasgger import Swagger
from MyFlask import MyFlask
from resources import item_Bp, user_Bp
from flask_jwt import JWT
from services import authenticate, identity

swagger_template = {
    # Other settings
    "securityDefinitions": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    # Other settings
}


def create_app(test_config=None):

    app = MyFlask(__name__)
    app.secret_key = "jacek"
    jwt = JWT(app, authenticate, identity)  # noqa
    swagger = Swagger(app, template=swagger_template)  # noqa
    app.register_blueprint(item_Bp)
    app.register_blueprint(user_Bp)
    return app
