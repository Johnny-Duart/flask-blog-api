from http import HTTPStatus

from flask import Blueprint, request

from flask_blog_api.models import Role, db

app = Blueprint("role", __name__, url_prefix="/roles")


@app.route("/", methods=["POST"])
@jwt_required()
@requires_role("admin")
def create_role():
    """
    ---
    post:
      tags:
        - Roles
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
      responses:
        200:
          description: Criar cargos
    """
    data = request.json
    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()
    return {"message": "role created!"}, HTTPStatus.CREATED


def list_role():
    query = db.select(Role)
    roles = db.session.execute(query).scalars()

    return [
        {
            "name": role.name,
            "id": role.id,
        }
        for role in roles
    ]


@app.route("/", methods=["GET"])
@requires_role("admin")
def list_roles():
    """
    ---
    get:
      tags:
        - Roles
      responses:
        200:
          description: Lista de cargos
    """
    return {"roles:": list_role()}
