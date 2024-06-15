from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from news.models import News


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.news = News.objects.create(title='Заголовок', text='Текст')

    def test_home_page(self):
        url = reverse('news:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_detail_page(self):
        url = reverse('news:detail', args=(self.news.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


# =============================================================================
# Страница отдельной новости доступна анонимному пользователю.
# Страницы удаления и редактирования комментария доступны автору комментария.
# При попытке перейти на страницу редактирования или удаления комментария анонимный пользователь перенаправляется на страницу авторизации.
# Авторизованный пользователь не может зайти на страницы редактирования или удаления чужих комментариев (возвращается ошибка 404).
# Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны анонимным пользователям.
# =============================================================================
