from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from .conftest import (CLIENT_AUTHOR, CLIENT_DEFAULT, CLIENT_NOT_AUTHOR,
                       COMMENT_DELETE_URL, COMMENT_UPDATE_URL, NEWS_DETAIL_URL,
                       NEWS_HOME_URL, USERS_LOGIN_URL, USERS_LOGOUT_URL,
                       USERS_SIGNUP_URL)


@pytest.mark.parametrize(
    'parametrized_client, url, expected_status',
    (
        (CLIENT_DEFAULT, NEWS_HOME_URL, HTTPStatus.OK),
        (CLIENT_DEFAULT, NEWS_DETAIL_URL, HTTPStatus.OK),
        (CLIENT_DEFAULT, USERS_LOGIN_URL, HTTPStatus.OK),
        (CLIENT_DEFAULT, USERS_LOGOUT_URL, HTTPStatus.OK),
        (CLIENT_DEFAULT, USERS_SIGNUP_URL, HTTPStatus.OK),
        (CLIENT_NOT_AUTHOR, COMMENT_UPDATE_URL, HTTPStatus.NOT_FOUND),
        (CLIENT_NOT_AUTHOR, COMMENT_DELETE_URL, HTTPStatus.NOT_FOUND),
        (CLIENT_AUTHOR, COMMENT_UPDATE_URL, HTTPStatus.OK),
        (CLIENT_AUTHOR, COMMENT_DELETE_URL, HTTPStatus.OK),
        (CLIENT_NOT_AUTHOR, COMMENT_UPDATE_URL, HTTPStatus.NOT_FOUND),
        (CLIENT_NOT_AUTHOR, COMMENT_DELETE_URL, HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability(parametrized_client, url, expected_status):
    """
    Главная страница доступна анонимному пользователю.

    Страницы регистрации пользователей, входа в учётную запись и выхода из неё
    доступны анонимным пользователям.

    Страница отдельной новости доступна анонимному пользователю.

    Страницы удаления и редактирования комментария доступны автору
    комментария.

    Авторизованный пользователь не может зайти на страницы редактирования или
    удаления чужих комментариев (возвращается ошибка 404).

    Авторизованный пользователь не может редактировать чужие комментарии.

    Авторизованный пользователь не может удалять чужие комментарии.

    """
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (COMMENT_UPDATE_URL, COMMENT_DELETE_URL)
)
def test_redirect_for_anonymous_client(client, url, users_login_url):
    """
    При попытке перейти на страницу редактирования или удаления комментария
    анонимный пользователь перенаправляется на страницу авторизации.

    """
    expected_url = f'{users_login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
