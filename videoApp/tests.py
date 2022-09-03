from time import sleep

from rest_framework import status
from django.test import TestCase
from django.urls import reverse

from videoApp.models import Video


# Create your tests here.
class VideoViewSetTest(TestCase):
    """Tests videos endpoint"""

    @classmethod
    def setUpTestData(cls):
        """setup DB with test data"""
        cls.vids = [
            Video(title="titl", description="desc", published_at="1", channel_title="C1"),
            Video(title="titl2", description="desc2", published_at="2", channel_title="C2"),
            Video(title="titl3", description="desc3", published_at="3", channel_title="C3"),
        ]
        for vid in cls.vids:
            vid.save()


    def test_get_vids(self):
        """Tests GET videos are sorted"""
        response = self.client.get(reverse("ytvideo-list"))
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        print(response.data['results'])
        self.assertEquals(len(self.vids), len(response.data['results']))
        self.assertEquals(response.data['results'][0]['published_at'], '3')


    # def test_fetching(self):
    #     """test whether videos are being fetched"""
    #     dbsize = Video.objects.count()
    #     sleep(62)
    #     self.assertNotEqual(dbsize, Video.objects.count())
