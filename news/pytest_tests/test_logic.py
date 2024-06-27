from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError, assertRedirects

from .constants import COMMENT_TEXT, FORM_DATA, FORM_DATA_NEW, NEW_COMMENT_TEXT


def test_anonymous_user_cant_create_comment(client, news_detail_url):
    """Анонимный пользователь не может отправить комментарий."""
    comments_count_init = Comment.objects.count()
    client.post(news_detail_url, data=FORM_DATA)
    comments_count = Comment.objects.count()
    assert comments_count == comments_count_init


def test_user_can_create_comment(author_client, author, news, news_detail_url):
    """Авторизованный пользователь может отправить комментарий."""
    comments_count_init = Comment.objects.count()
    response = author_client.post(news_detail_url, data=FORM_DATA)
    assertRedirects(response, f'{news_detail_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == comments_count_init + 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, news_detail_url):
    """
    Если комментарий содержит запрещённые слова, он не будет опубликован, а
    форма вернёт ошибку.

    """
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, ещё текст'}
    comments_count_init = Comment.objects.count()
    response = author_client.post(news_detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == comments_count_init


def test_author_can_edit_comment(
    author_client, comment, news_detail_url, comment_update_url
):
    """Авторизованный пользователь может редактировать свои комментарии."""
    response = author_client.post(comment_update_url, data=FORM_DATA_NEW)
    url_to_comments = news_detail_url + '#comments'
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == NEW_COMMENT_TEXT


def test_author_can_delete_comment(
    author_client, news_detail_url, comment_delete_url
):
    """Авторизованный пользователь может удалять свои комментарии."""
    comments_count_init = Comment.objects.count()
    response = author_client.delete(comment_delete_url)
    url_to_comments = news_detail_url + '#comments'
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count + 1 == comments_count_init


def test_user_cant_edit_comment_of_another_user(
    not_author_client, comment, comment_update_url
):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    not_author_client.post(comment_update_url, data=FORM_DATA_NEW)
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT


def test_user_cant_delete_comment_of_another_user(
    not_author_client, comment_delete_url
):
    """Авторизованный пользователь не может удалять чужие комментарии."""
    comments_count_init = Comment.objects.count()
    not_author_client.delete(comment_delete_url)
    comments_count = Comment.objects.count()
    assert comments_count == comments_count_init
