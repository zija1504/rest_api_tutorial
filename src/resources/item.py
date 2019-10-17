from flasgger import swag_from
from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt import jwt_required
from marshmallow import ValidationError
from model.item import ItemModel
from schema import ItemGetSchema, ItemPostSchema

item_Bp = Blueprint("item", __name__)


class Item(MethodView):
    @jwt_required()
    @swag_from("../swagger/item/get.yaml")
    def get(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"message": "item does not exist"}, 404

    @jwt_required()
    @swag_from("../swagger/item/post.yaml")
    def post(self, name):
        data = request.get_json()
        try:
            data_json = ItemPostSchema().load(data)
        except ValidationError as err:
            return err.messages
        if ItemModel.find_by_name(name):
            return (
                {
                    "message": "An item with name '{}' already exists.".format(
                        name
                    )
                },
                404,
            )
        else:
            item = ItemModel(name, data_json["price"], data_json["store_id"])
            item.save_to_db()
            return item.json(), 201

    @jwt_required()
    @swag_from("../swagger/item/delete.yaml")
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "item deleted"}

    @jwt_required()
    @swag_from("../swagger/item/put.yaml")
    def put(self, name):
        data = request.get_json()
        try:
            data_json = ItemPostSchema().load(data)
        except ValidationError as err:
            return err.messages
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data_json["price"]
            item.store_id = data_json["store_id"]
        else:
            item = ItemModel(name, data_json["price"], data_json["store_id"])
        item.save_to_db()
        return {"message": "item was succesfully created/updated"}, 201


class Items(MethodView):
    @swag_from("../swagger/items/get_items.yaml")
    def get(self):
        items: list[any] = ItemModel.query.all()
        return ItemGetSchema(many=True).dump(items)


item_Bp.add_url_rule("/item/<name>", view_func=Item.as_view("item"))
item_Bp.add_url_rule("/item", view_func=Items.as_view("items"))
