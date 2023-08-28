from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("", views.home, name="home"),
    path("en/words/", views.english_list, name="english-list"),
    path("en/words/<word>/", views.english_detail, name="english-detail"),
    path("en/games/", views.game_list, name="game-list"),
    path("en/games/single-word/", views.single_word_detail, name="single-word-detail"),
    path(
        "en/games/single-word/start/", views.single_word_start, name="single-word-start"
    ),
    path("en/wordboxes/", views.wordbox_list, name="wordbox-list"),
    path("en/wordboxes/<int:pk>/", views.wordbox_detail, name="wordbox-detail"),
    path("en/wordboxes/<int:pk>/start/", views.wordbox_start, name="wordbox-start"),
]
