from typing import Optional, List, Dict
from unittest.mock import patch

from django.urls import reverse
from rest_framework.test import APITestCase

from justworktrial.settings import ADMIN_USERNAME, ADMIN_PASSWORD
from pages.models import Page, Video, Audio, Text


class PagesTests(APITestCase):
    page: Optional[Page] = None
    fake_url = "http://test.com"
    video: Optional[Video] = None
    audio: Optional[Audio] = None
    text: Optional[Text] = None


    def setUp(self) -> None:
        self.page = Page.objects.create(title='Test page')
        self.video = Video.objects.create(
            title="Test video",
            video_file_link=self.fake_url,
            subtitles_file_link=self.fake_url
        )
        self.audio = Audio.objects.create(title='Test audio', bit_rate=256)
        self.text = Text.objects.create(title='test', body="Test text")

    def get_pages(self, username: Optional[str] = ADMIN_USERNAME, password: Optional[str] = ADMIN_PASSWORD) -> List[Dict]:
        """Получает через пагинацию все ссылки на все страницы."""

        if username and password:
            self.client.login(username=username, password=password)

        url = reverse('list-pages')
        results = []
        while True:
            response = self.client.get(url)
            results += response.data['results']
            if not response.data['next']:
                break
            else:
                url = response.data['next']
        return results

    def get_page(self, page_id: int) -> Dict:
        pages = self.get_pages()
        filtered = [x for x in pages if x['id'] == page_id]
        self.assertEquals(len(filtered), 1)
        self.assertEquals(filtered[0]['id'], self.page.id)
        return filtered[0]

    def get_page_details(
            self,
            page_id: int,
            username: Optional[str] = ADMIN_USERNAME,
            password: Optional[str] = ADMIN_PASSWORD
    ) -> Dict:
        if username and password:
            self.client.login(username=username, password=password)

        url = reverse('page-detail', kwargs=dict(pk=page_id))
        response = self.client.get(url)
        return response.data

    def test_page_is_listed(self):
        """Созданная в базе страница, должна быть доступна через API."""

        page = self.get_page(self.page.id)
        self.assertEquals(page['title'], self.page.title)

    def test_page_videos_are_linked(self):
        """Связанные со страницей видео должны быть доступны через API деталей страницы."""

        self.page.videos.add(self.video)
        page = self.get_page_details(self.page.id)
        self.assertEquals(len(page['contents']), 1)
        self.assertEquals(page['contents'][0]['id'], self.video.id)
        self.assertEquals(page['contents'][0]['title'], self.video.title)
        self.assertEquals(page['contents'][0]['video_file_link'], self.video.video_file_link)
        self.assertEquals(page['contents'][0]['subtitles_file_link'], self.video.subtitles_file_link)

    def test_page_audios_are_linked(self):
        """Связанные со страницей аудио должны быть доступны через API деталей страницы."""

        self.page.audios.add(self.audio)
        page = self.get_page_details(self.page.id)
        self.assertEquals(len(page['contents']), 1)
        self.assertEquals(page['contents'][0]['id'], self.audio.id)
        self.assertEquals(page['contents'][0]['title'], self.audio.title)
        self.assertEquals(page['contents'][0]['bit_rate'], self.audio.bit_rate)

    def test_page_texts_are_linked(self):
        """Связанные со страницей тексты должны быть доступны через API деталей страницы."""

        self.page.texts.add(self.text)
        page = self.get_page_details(self.page.id)
        self.assertEquals(len(page['contents']), 1)
        self.assertEquals(page['contents'][0]['id'], self.text.id)
        self.assertEquals(page['contents'][0]['title'], self.text.title)
        self.assertEquals(page['contents'][0]['body'], self.text.body)

    @patch('pages.views.update_page_content_counters')
    def test_celery_task_for_counters_update_is_triggered(self, task_mock):
        self.get_page_details(self.page.id)
        self.assertEquals(len(task_mock.method_calls), 1)
        self.assertEquals(task_mock.method_calls[0][0], 'delay')
        self.assertEquals(task_mock.method_calls[0][2], dict(page_id=self.page.id))
