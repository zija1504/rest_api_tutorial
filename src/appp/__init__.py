from datetime import timedelta
import os
from flasgger import Swagger
from flask import jsonify
from flask_jwt import JWT
from model.database import db
from MyFlask import MyFlask
from resources import item_Bp, user_Bp, store_Bp
from services import authenticate
from services import identity as identity_function

swagger_template = {
    # Other settings
    "securityDefinitions": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    }
}
jwt = JWT(
    authentication_handler=authenticate, identity_handler=identity_function
)  # noqa

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(test_config=None):

    app = MyFlask(__name__)
    app.secret_key = "jacek"
    app.config["JWT_AUTH_URL_RULE"] = "/login"
    app.config["JWT_AUTH_HEADER_NAME"] = "JWT"
    app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data.db")

    @app.before_first_request
    def create_tables():
        db.create_all()

    jwt.init_app(app)
    db.init_app(app)
    swagger = Swagger(app, template=swagger_template)  # noqa
    app.register_blueprint(item_Bp)
    app.register_blueprint(user_Bp)
    app.register_blueprint(store_Bp)

    @jwt.auth_response_handler
    def customized_response_handler(access_token, identity):
        return jsonify(
            {
                "access_token": access_token.decode("utf-8"),
                "user_id": identity.id,
            }
        )

    @jwt.jwt_error_handler
    def customized_error_handler(error):
        return (
            jsonify({"message": error.description, "code": error.status_code}),
            error.status_code,
        )

    return app
