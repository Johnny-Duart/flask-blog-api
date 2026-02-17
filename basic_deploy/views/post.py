from basic_deploy.app import ma
from basic_deploy.models import Post
from marshmallow import fields


class PostSchema(ma.SQLAlchemyAutoSchema):
    title = ma.auto_field()
    body = ma.auto_field()
    author_id = ma.auto_field()

    class Meta:
        model = Post
        ordered = True
        fields = ("title", "body", "author_id")
        load_instance = True


class CreatePostSchema(ma.Schema):
    title = fields.String(required=True)
    body = fields.String(required=True)


class UpdatePostSchema(ma.Schema):
    title = fields.String(required=False)
    body = fields.String(required=False)
