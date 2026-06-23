from marshmallow import fields

from flask_blog_api.app import ma
from flask_blog_api.models import Role


class RoleSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Role
        fields = ("id", "name")
        load_instance = True
