# =============================================================================
# Авторизованный пользователь может отправить комментарий.
# Если комментарий содержит запрещённые слова, он не будет опубликован, а форма вернёт ошибку.
# Авторизованный пользователь может редактировать или удалять свои комментарии.
# Авторизованный пользователь не может редактировать или удалять чужие комментарии.
# =============================================================================

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from news.models import Comment, News

User = get_user_model()


class TestCommentCreation(TestCase):

    COMMENT_TEXT = 'Текст комментария'

    @classmethod
    def setUpTestData(cls) -> None:
        cls.news = News.objects.create(title='Заголовок', text='Текст')
        cls.url = reverse('news:detail', args=(cls.news.id,))
        cls.user = User.objects.create(username='Мимо Крокодил')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {'text': cls.COMMENT_TEXT}

    def test_anonymous_user_cant_create_comment(self):
        self.client.post(self.url, data=self.form_data)
        comments_count = Comment.objects.count()
        self.assertEqual(comments_count, 0)
