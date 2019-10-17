from flasgger import swag_from
from flask import Blueprint
from flask.views import MethodView
from flask_jwt import jwt_required
from model import StoreModel
from schema.store import StoreGetSchema

store_Bp = Blueprint("store", __name__)


class Store(MethodView):
    @jwt_required()
    @swag_from("../swagger/store/get.yaml")
    def get(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {"message": "store does not exist"}, 404

    @jwt_required()
    @swag_from("../swagger/store/post.yaml")
    def post(self, name):
        if StoreModel.find_by_name(name):
            return (
                {
                    "message": "An store with name '{}' already exists.".format(
                        name
                    )
                },
                400,
            )
        else:
            store = StoreModel(name)
        try:
            store.save_to_db()
            return {"message": "store was succesfully created"}, 201
        except Exception:
            return (
                {"message": "An error occurred while creating the store"},
                500,
            )

    @jwt_required()
    @swag_from("../swagger/store/delete.yaml")
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "Store deleted"}


class Stores(MethodView):
    @swag_from("../swagger/stores/get.yaml")
    def get(self):
        stores = StoreModel.query.all()
        stores_json = StoreGetSchema(many=True).dump(stores)
        print(stores_json)
        return stores_json


store_Bp.add_url_rule("/store", view_func=Stores.as_view("stores"))
store_Bp.add_url_rule("/store/<name>", view_func=Store.as_view("store"))
