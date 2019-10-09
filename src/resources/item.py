from flask.views import MethodView
from flask import Blueprint, request
from schema import ItemGetSchema, ItemPostSchema
from flasgger import swag_from
from flask_jwt import jwt_required

item_Bp = Blueprint("item", __name__)

itemsList = [{"name": "box", "price": 12.99}]


class Item(MethodView):
    @jwt_required()
    @swag_from("../swagger/item/get.yaml")
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, itemsList), None)
        item_json = ItemGetSchema().dump(item)
        return item_json

    @jwt_required()
    @swag_from("../swagger/item/post.yaml")
    def post(self, name):
        if (
            next(filter(lambda x: x["name"] == name, itemsList), None)
            is not None
        ):
            return {
                "message": "An item with name '{}' already exists.".format(name)
            }
        data = request.get_json()
        data_json = ItemPostSchema().load(data)
        item = {"name": name, "price": data_json["price"]}
        itemsList.append(item)
        return item, 201

    @jwt_required()
    @swag_from("../swagger/item/delete.yaml")
    def delete(self, name):
        try:
            itemsList.remove(
                next(filter(lambda x: x["name"] == name, itemsList))
            )
            return {"message": "Item deleted"}, 200
        except ValueError:
            return {"error": "item not on the list"}, 404

    @jwt_required()
    @swag_from("../swagger/item/put.yaml")
    def put(self, name):
        data = request.get_json()
        print(data)
        data_json = ItemPostSchema().load(data)
        item = next(filter(lambda x: x["name"] == name, itemsList), None)
        if item is None:
            item = {"name": name, "price": data_json["price"]}
            itemsList.append(item)
        else:
            item.update(data)
        return item


item_Bp.add_url_rule("/item/<name>", view_func=Item.as_view("item"))
