from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from flask_blog_api.controllers.utils import requires_role
from flask_blog_api.models import Post, db
from flask_blog_api.views.post import (
    CreatePostSchema,
    PostSchema,
    UpdatePostSchema,
)

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


@app.route("/", methods=["POST"])
@jwt_required()
def create_posts():
    """
    ---
    post:
      tags:
        - Posts
      summary: Criar novo post
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - title
                - body
              properties:
                title:
                  type: string
                body:
                  type: string
      responses:
        201:
          description: Post criado com sucesso
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                  title:
                    type: string
                  body:
                    type: string
                  author_id:
                    type: integer
        422:
          description: Erro de validação
    """

    author_id = get_jwt_identity()
    response = _create_post(author_id)
    if response:
        return response
    return {"message": "post created!"}, HTTPStatus.CREATED


@app.route("/", methods=["GET"])
def list_post():
    """
    ---
    get:
      tags:
        - Posts
      security: []
      summary: Listar todos os posts
      responses:
        200:
          description: Lista de posts
    """

    return {"posts:": _list_post()}


@app.route("/<int:post_id>", methods=["PATCH"])
def update_post(post_id):
    """
    ---
    patch:
      tags:
        - Posts
      summary: Atualizar post
      parameters:
        - in: path
          name: post_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
                body:
                  type: string
      responses:
        200:
          description: Post atualizado com sucesso
        404:
          description: Post não encontrado
    """
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
    """
    ---
    delete:
      tags:
        - Posts
      summary: Deletar post
      parameters:
        - in: path
          name: post_id
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Post deletado com sucesso
        404:
          description: Post não encontrado
    """
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
