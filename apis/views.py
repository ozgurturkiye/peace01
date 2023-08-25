from django.urls import reverse

from rest_framework.response import Response
from rest_framework.decorators import api_view

from words.models import English
from .serializers import EnglishSerializer


@api_view()
def home(request):
    return Response({"detail": "Welcome to home page"})


@api_view(["GET"])
def english_list(request):
    words = English.objects.all()
    serializer = EnglishSerializer(words, many=True)
    return Response(serializer.data)
