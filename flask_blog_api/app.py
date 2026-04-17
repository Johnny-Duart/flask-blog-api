import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, json
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from werkzeug.exceptions import HTTPException

from flask_blog_api.models.base import db

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
    app.config.from_object(
        f"flask_blog_api.config.{environment.title()}Config"
    )
    app.json.sort_keys = False

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    from flask_blog_api.controllers import auth, post, role, user

    app.register_blueprint(post.app)
    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    spec = APISpec(
        title="Flask_blog_api",
        version="1.0.0",
        openapi_version="3.0.3",
        info=dict(description="Flask_blog_api"),
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )
    spec.options["security"] = [{"BearerAuth": []}]
    spec.components.security_scheme(
        "BearerAuth",
        {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        },
    )

    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint != "static":
                view = app.view_functions[rule.endpoint]
                spec.path(view=view)

    @app.route("/swagger.json")
    def swagger_json():
        return spec.to_dict()

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
