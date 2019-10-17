from marshmallow import fields, Schema
from .item import ItemGetSchema


class StoreGetSchema(Schema):
    name = fields.Str(required=True)
    items = fields.List(fields.Nested(ItemGetSchema))


class StorePostSchema(Schema):
    price = fields.Float(required=True)
    store = fields.Int(required=True)
