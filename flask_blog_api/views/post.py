from marshmallow import fields

from flask_blog_api.app import ma
from flask_blog_api.models import Post


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
