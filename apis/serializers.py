from rest_framework import serializers

from words.models import English, Game, WordBox, WordBoxDetail, Turkish


class TurkishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turkish
        fields = ["id", "name"]


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


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "name",
        ]


class SingleWordSerializer(serializers.Serializer):
    english = serializers.CharField(max_length=50)
    turkish = serializers.CharField(max_length=50)


class WordBoxSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = WordBox
        fields = ["id", "name", "owner", "created_at", "words", "users"]


class WordBoxDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordBoxDetail
        fields = ["id", "wordbox", "english", "user", "answer_status", "updated_at"]


class WordBoxGameEnglishSerializer(serializers.ModelSerializer):
    translations = TurkishSerializer(read_only=True, many=True)

    class Meta:
        model = English
        fields = ["id", "name", "translations"]


class WordBoxGameInputSerializer(serializers.Serializer):
    turkish = serializers.CharField(max_length=50)


class WordBoxWordSerializer(serializers.Serializer):
    """This is a List serializer for WordBoxWord"""

    words = serializers.ListSerializer(child=serializers.CharField(max_length=50))
