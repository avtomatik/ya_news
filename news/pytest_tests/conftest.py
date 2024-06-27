from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
from news.models import Comment, News


@pytest.fixture(autouse=True)
def autouse_db(db):
    ...


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(db):
    news = News.objects.create(
        title='Тестовая новость',
        text='Просто текст.',
        date=datetime.today()
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def news_on_page(db):
    today = datetime.today()
    return News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comments_to_news(author, news):
    now = timezone.now()
    return Comment.objects.bulk_create(
        Comment(
            news=news,
            author=author,
            text=f'Текст {index}',
            created=now + timedelta(days=index)
        )
        for index in range(10)
    )


@pytest.fixture
def comment_update_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def comment_delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def news_home_url():
    return reverse('news:home')


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def users_login_url():
    return reverse('users:login')


@pytest.fixture
def users_logout_url():
    return reverse('users:logout')


@pytest.fixture
def users_signup_url():
    return reverse('users:signup')


CLIENT_DEFAULT = pytest.lazy_fixture('client')

CLIENT_NOT_AUTHOR = pytest.lazy_fixture('not_author_client')

CLIENT_AUTHOR = pytest.lazy_fixture('author_client')

COMMENT_UPDATE_URL = pytest.lazy_fixture('comment_update_url')

COMMENT_DELETE_URL = pytest.lazy_fixture('comment_delete_url')

NEWS_HOME_URL = pytest.lazy_fixture('news_home_url')

NEWS_DETAIL_URL = pytest.lazy_fixture('news_detail_url')

USERS_LOGIN_URL = pytest.lazy_fixture('users_login_url')

USERS_LOGOUT_URL = pytest.lazy_fixture('users_logout_url')

USERS_SIGNUP_URL = pytest.lazy_fixture('users_signup_url')
