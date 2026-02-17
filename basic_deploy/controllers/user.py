from http import HTTPStatus

from basic_deploy.app import bcrypt
from basic_deploy.controllers.utils import requires_role
from basic_deploy.models import User, db
from basic_deploy.views.user import (
    CreateUserSchema,
    UpdateUserSchema,
    UserSchema,
)
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

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


@app.route("/", methods=["GET"])
@jwt_required()
@requires_role("admin")
def list_users():
    return {"users": _list_users()}


@app.route("/", methods=["POST"])
def create_users():
    response = _create_user()
    if response:
        return response
    return {"message": "user created!"}, HTTPStatus.CREATED


@app.route("/<int:user_id>")
@jwt_required()
@requires_role("admin")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username,
    }


# patch = alteração parcial
# put = alteração completa
@app.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    update_schema = UpdateUserSchema()
    data = update_schema.load(request.json)

    if "username" in data:
        user.username = data["username"]

    if "id" in data:
        user.id = data["id"]

    db.session.commit()
    return UserSchema().dump(user), HTTPStatus.OK


@app.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
