from django.test import TestCase

from words.models import English


class EnglishTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.english = English.objects.create(name="abandon", word_type="V")

    def test_english_content(self):
        self.assertEqual(self.english.name, "abandon", "“Why, Mr. Anderson?, Why, why?")
        self.assertEqual(self.english.word_type, "V")
