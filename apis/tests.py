from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from words.models import English


class EnglishModelTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.english = English.objects.create(
            name="abandon",
            word_type="V",
        )

    def test_model_content(self):
        self.assertEqual(self.english.name, "abandon")
        self.assertEqual(self.english.word_type, "V")
        self.assertEqual(str(self.english.name), "abandon")

    # def test_api_english_listview(self):
    #     response = self.client.get(reverse("api:english-list"))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(English.objects.count(), 1)
    #     self.assertContains(response, self.english)
