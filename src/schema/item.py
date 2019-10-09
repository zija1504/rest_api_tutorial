from marshmallow import fields, Schema


class ItemGetSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class ItemPostSchema(Schema):
    price = fields.Float(required=True)
