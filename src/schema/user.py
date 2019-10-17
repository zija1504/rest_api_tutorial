from marshmallow import (
    fields,
    Schema,
    validate,
    validates_schema,
    ValidationError,
)


class UserSchema(Schema):
    username = fields.Str(required=True)
    password_check = fields.Str(required=True)
    password = fields.Str(
        required=True, validate=[validate.Length(min=6, max=36)]
    )

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if data["password_check"] != data["password"]:
            raise ValidationError("retype password, not equal")


class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(
        required=True, validate=[validate.Length(min=6, max=36)]
    )
