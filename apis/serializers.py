from rest_framework import serializers

from words.models import English


class EnglishSerializer(serializers.ModelSerializer):
    class Meta:
        model = English
        fields = [
            "id",
            "name",
            "synonyms",
            "translations",
            "word_type",
        ]
