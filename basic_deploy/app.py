import os

from basic_deploy.models.base import db
from flask import Flask, json
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()


def create_app(environment=os.environ["ENVIRONMENT"]):
    app = Flask(
        __name__,
        instance_path=os.path.join(os.path.dirname(__file__), "instance"),
        instance_relative_config=False,
    )
    app.config.from_object(f"basic_deploy.config.{environment.title()}Config")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    from basic_deploy.controllers import auth, post, role, user

    app.register_blueprint(post.app)
    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    @app.errorhandler(HTTPException)
    def handle_exception(a):
        response = a.get_response()
        response.data = json.dumps(
            {
                "Code:": a.code,
                "Descrição:": a.description,
                "Nome:": a.name,
            }
        )
        response.content_type = "application/json"
        return response

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
    app.run()
