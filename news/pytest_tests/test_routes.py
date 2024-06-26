from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from .constants import FORM_DATA_NEW


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('client'), HTTPStatus.OK),
    )
)
@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('news_home_url'),
        pytest.lazy_fixture('news_detail_url'),
        pytest.lazy_fixture('users_login_url'),
        pytest.lazy_fixture('users_logout_url'),
        pytest.lazy_fixture('users_signup_url')
    )
)
def test_pages_availability_for_anonymous_user(
    parametrized_client, url, expected_status
):
    """
    Главная страница доступна анонимному пользователю.

    Страницы регистрации пользователей, входа в учётную запись и выхода из неё
    доступны анонимным пользователям.

    Страница отдельной новости доступна анонимному пользователю.

    """
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    )
)
@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('comment_update_url'),
        pytest.lazy_fixture('comment_delete_url')
    )
)
def test_pages_availability_for_different_users(
    parametrized_client, url, expected_status
):
    """
    Страницы удаления и редактирования комментария доступны автору
    комментария.

    Авторизованный пользователь не может зайти на страницы редактирования или
    удаления чужих комментариев (возвращается ошибка 404).

    """
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


def test_user_cant_edit_comment_of_another_user(
    not_author_client, comment_update_url
):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    response = not_author_client.post(comment_update_url, data=FORM_DATA_NEW)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_user_cant_delete_comment_of_another_user(
    not_author_client, comment_delete_url
):
    """Авторизованный пользователь не может удалять чужие комментарии."""
    response = not_author_client.delete(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('comment_update_url'),
        pytest.lazy_fixture('comment_delete_url')
    )
)
def test_redirect_for_anonymous_client(client, url, users_login_url):
    """
    При попытке перейти на страницу редактирования или удаления комментария
    анонимный пользователь перенаправляется на страницу авторизации.

    """
    expected_url = f'{users_login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
