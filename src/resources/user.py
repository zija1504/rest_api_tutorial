import sqlite3
from flask.views import MethodView
from flasgger import swag_from
from flask import Blueprint, request
from schema import UserSchema
from marshmallow import ValidationError

user_Bp = Blueprint("user", __name__)


class UserRegister(MethodView):
    @swag_from("../swagger/user/post.yaml")
    def post(self):
        connection = sqlite3.Connection("src/data.db")
        cursor = connection.cursor()
        data_load = request.get_json()
        try:
            data = UserSchema().load(data_load)
            query = "SELECT * FROM users WHERE username=?"
            result = cursor.execute(query, (data["username"],))
            if result.fetchone() is None:
                query = "INSERT INTO users VALUES (NULL, ?, ?)"
                cursor.execute(query, (data["username"], data["password"]))
                connection.commit()
                connection.close()
                return {"response": "The user was successfuly created"}, 201
            else:
                return {"error": "User with this username already exist"}
        except ValidationError as err:
            return err.messages, 404


user_Bp.add_url_rule("/register", view_func=UserRegister.as_view("register"))
