from basic_deploy.app import ma
from basic_deploy.models import Role
from marshmallow import fields


class RoleSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Role
        fields = ("id", "name")
        load_instance = True
