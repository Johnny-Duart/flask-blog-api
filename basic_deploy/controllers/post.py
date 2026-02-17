from http import HTTPStatus

from basic_deploy.controllers.utils import requires_role
from basic_deploy.models import Post, db
from basic_deploy.views.post import (
    CreatePostSchema,
    PostSchema,
    UpdatePostSchema,
)
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

app = Blueprint("post", __name__, url_prefix="/posts")


def _create_post(author_id):
    try:
        data = CreatePostSchema().load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    post = Post(
        title=data["title"],
        body=data["body"],
        author_id=author_id,
    )

    db.session.add(post)
    db.session.commit()

    return PostSchema().dump(post), HTTPStatus.CREATED


def _list_post():
    query = db.select(Post)
    posts = db.session.execute(query).scalars().all()
    posts_schema = PostSchema(many=True)

    return posts_schema.dump(posts)


@app.route("/", methods=["GET"])
def list_post():
    return {"posts:": _list_post()}


@app.route("/", methods=["POST"])
@jwt_required()
def create_posts():
    author_id = get_jwt_identity()
    response = _create_post(author_id)
    if response:
        return response
    return {"message": "post created!"}, HTTPStatus.CREATED


@app.route("/<int:post_id>", methods=["PATCH"])
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    update_schema = UpdatePostSchema()
    data = update_schema.load(request.json)

    if "title" in data:
        post.title = data["title"]

    if "body" in data:
        post.body = data["body"]

    db.session.commit()

    return PostSchema().dump(post), HTTPStatus.OK


@app.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
