from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("", views.home, name="home"),
    path("login-test-page/", views.login_test_page, name="login-text-page"),
    path("en/words/", views.english_list, name="english-list"),
    path("en/words/<word>/", views.english_detail, name="english-detail"),
    path(
        "en/words/<word>/synonyms/",
        views.english_synonyms_list,
        name="english-synonyms-list",
    ),
    path(
        "en/words/<word>/translations/",
        views.english_translation_list,
        name="english-translation-list",
    ),
    path("en/games/", views.game_list, name="game-list"),
    path("en/games/single-word/", views.single_word_detail, name="single-word-detail"),
    path(
        "en/games/single-word/start/", views.single_word_start, name="single-word-start"
    ),
    path("en/wordboxes/", views.wordbox_list, name="wordbox-list"),
    path("en/wordboxes/<int:pk>/", views.wordbox_detail, name="wordbox-detail"),
    path("en/wordboxes/<int:pk>/start/", views.wordbox_start, name="wordbox-start"),
    path(
        "en/wordboxes/<int:pk>/words/",
        views.wordbox_word_list,
        name="wordbox-word-list",
    ),
    path(
        "en/wordboxes/<int:pk>/users/",
        views.wordbox_user_list,
        name="wordbox-user-list",
    ),
]
