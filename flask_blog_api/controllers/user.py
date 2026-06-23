from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from flask_blog_api.app import bcrypt
from flask_blog_api.controllers.utils import requires_role
from flask_blog_api.models import User, db
from flask_blog_api.views.user import (
    CreateUserSchema,
    UpdateUserSchema,
    UserSchema,
)

app = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    user_schema = CreateUserSchema()
    try:
        data = user_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]),
        role_id=data["role_id"],
    )

    db.session.add(user)
    db.session.commit()


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    users_schema = UserSchema(many=True)
    return users_schema.dump(users)


@app.route("/", methods=["POST"])
def create_users():
    """
    ---
    post:
      tags:
        - Users
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                password:
                  type: string
      responses:
        200:
          description: Criar usuarios
    """

    response = _create_user()
    if response:
        return response
    return {"message": "user created!"}, HTTPStatus.CREATED


@app.route("/", methods=["GET"])
@jwt_required()
@requires_role("admin")
def list_users():
    """
    ---
    get:
      tags:
        - Users
      responses:
        200:
          description: Lista de usuários
    """
    return {"users": _list_users()}


# patch = alteração parcial
# put = alteração completa
@app.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    """
    ---
    patch:
      tags:
        - Users
      parameters:
        - in: path
          name: user_id
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
                username:
                  type: string
                password:
                  type: string
      responses:
        200:
          description: Atualizar usuarios
    """
    user = db.get_or_404(User, user_id)
    update_schema = UpdateUserSchema()
    data = update_schema.load(request.json)

    if "username" in data:
        user.username = data["username"]

    if "password" in data:
        user.password = bcrypt.generate_password_hash(data["password"])

    db.session.commit()
    return UserSchema().dump(user), HTTPStatus.OK


@app.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    ---
    delete:
      tags:
        - Users
      parameters:
        - in: path
          name: user_id
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Deleta usuarios
    """
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
