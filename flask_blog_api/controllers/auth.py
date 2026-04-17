from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from flask_blog_api.app import bcrypt
from flask_blog_api.models import User, db

app = Blueprint("auth", __name__, url_prefix="/auth")


@app.route("/login", methods=["POST"])
def login():
    """
    ---
    post:
      tags:
        - Auth
      security: []
      summary: Login do usuário
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - username
                - password
              properties:
                username:
                  type: string
                password:
                  type: string
      responses:
        200:
          description: Login realizado com sucesso
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
        401:
          description: Credenciais inválidas
    """

    username = request.json.get("username")
    password = request.json.get("password")
    user = db.session.execute(
        db.select(User).where(User.username == username)
    ).scalar()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return {"msg": "Credenciais incorretas"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}
    return {"access_token": access_token}
