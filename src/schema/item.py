from marshmallow import fields, Schema


class ItemGetSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Int()
    id = fields.Int()


class ItemPostSchema(Schema):
    price = fields.Float(required=True)
    store_id = fields.Int(required=True)
