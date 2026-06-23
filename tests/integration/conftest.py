import pytest

from flask_blog_api.app import bcrypt, create_app
from flask_blog_api.models import Role, User, db


@pytest.fixture
def app():
    app = create_app(environment="testing")
    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def access_token(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(
        username="Joel",
        password=bcrypt.generate_password_hash("1234"),
        role_id=role.id,
    )
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login",
        json={"username": user.username, "password": user.password},
    )
    return response.json["access_token"]
