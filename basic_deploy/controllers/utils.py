from functools import wraps
from http import HTTPStatus

from basic_deploy.models import User, db
from flask_jwt_extended import get_jwt_identity


def requires_role(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = int(get_jwt_identity())
            user = db.get_or_404(User, user_id)

            if user.role.name != role_name:
                return {
                    "message": "Usuario nao tem acesso"
                }, HTTPStatus.FORBIDDEN
            return f(*args, **kwargs)

        return wrapped

    return decorator
