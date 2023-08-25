from django.urls import reverse

from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view()
def home(request):
    return Response({"detail": "Welcome to home page"})
