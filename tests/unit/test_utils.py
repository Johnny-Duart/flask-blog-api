from http import HTTPStatus

import pytest

from flask_blog_api.controllers.utils import requires_role


def test_requires_role_success(mocker):

    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"
    mocker.patch("flask_blog_api.controllers.utils.get_jwt_identity")
    mocker.patch(
        "flask_blog_api.controllers.utils.db.get_or_404",
        return_value=mock_user,
    )
    decorated_function = requires_role("admin")(lambda: "Success")

    # When
    result = decorated_function()

    # Then
    assert result == "Success"


def test_requires_role_fail(mocker):

    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = "normal"
    mocker.patch("flask_blog_api.controllers.utils.get_jwt_identity")
    mocker.patch(
        "flask_blog_api.controllers.utils.db.get_or_404",
        return_value=mock_user,
    )
    decorated_function = requires_role("admin")(lambda: "Success")

    # When
    result, status = decorated_function()

    # Then
    assert status == HTTPStatus.FORBIDDEN
    assert result["message"] == "Usuario nao tem acesso"
