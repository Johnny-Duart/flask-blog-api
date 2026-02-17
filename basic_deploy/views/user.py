from basic_deploy.app import ma
from basic_deploy.models import User
from basic_deploy.views.role import RoleSchema
from marshmallow import fields


class UserSchema(ma.SQLAlchemyAutoSchema):
    role_id = fields.Integer()

    class Meta:
        model = User
        fields = ("id", "username", "role")
        load_instance = True

    role = ma.Nested(RoleSchema)


class CreateUserSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    role_id = fields.Integer(required=True, strict=True)

    class Meta:
        fields = ("username", "password", "role_id")


class UpdateUserSchema(ma.Schema):
    id = fields.String(required=False)
    username = fields.String(required=False)
