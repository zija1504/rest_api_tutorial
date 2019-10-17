from flasgger import swag_from
from flask import Blueprint, request
from flask.views import MethodView
from marshmallow import ValidationError

from schema import UserSchema
from model.user import UserModel


user_Bp = Blueprint("user", __name__)


class UserRegister(MethodView):
    @swag_from("../swagger/user/post.yaml")
    def post(self):
        data_load = request.get_json()
        try:
            data = UserSchema().load(data_load)
        except ValidationError as err:
            return err.messages, 404
        if UserModel.find_by_username(data["username"]) is None:
            user = UserModel(data["username"], data["password"])
            user.add_user()
            return {"response": "The user was successfuly created"}, 201
        else:
            return dict(error="User with this username already exist"), 500


class UserLogin(MethodView):
    @swag_from("../swagger/userLogin/post.yaml")
    def post(self):
        pass


user_Bp.add_url_rule("/login", view_func=UserLogin.as_view("login"))
user_Bp.add_url_rule("/register", view_func=UserRegister.as_view("register"))
