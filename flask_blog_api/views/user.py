from marshmallow import fields

from flask_blog_api.app import ma
from flask_blog_api.models import User
from flask_blog_api.views.role import RoleSchema


class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = User
        fields = ("id", "username", "role")
        load_instance = True

    role = ma.Nested(RoleSchema)


class UpdateUserParameter(ma.Schema):
    user_id = fields.String(required=True)


class CreateUserSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    role_id = fields.Integer(required=True, strict=True)

    class Meta:
        fields = ("username", "password", "role_id")


class UpdateUserSchema(ma.Schema):
    username = fields.String(required=False)
    password = fields.String(required=False)
