
# =============================================================================
# Новости отсортированы от самой свежей к самой старой. Свежие новости в начале списка.
# Комментарии на странице отдельной новости отсортированы от старых к новым: старые в начале списка, новые — в конце.
# Анонимному пользователю недоступна форма для отправки комментария на странице отдельной новости, а авторизованному доступна.
# =============================================================================

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from news.models import News


class TestHomePage(TestCase):

    HOME_URL = reverse('news:home')

    @classmethod
    def setUpTestData(cls) -> None:
        News.objects.bulk_create(
            News(title=f'Новость {index}', text='Просто текст.')
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        )

    def test_news_count(self):
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        news_count = object_list.count()
        self.assertEqual(news_count, settings.NEWS_COUNT_ON_HOME_PAGE)
