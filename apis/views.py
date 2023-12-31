from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from words.models import English, Game, SingleWordGame, WordBox, WordBoxDetail, Turkish
from .serializers import (
    TurkishSerializer,
    EnglishSerializer,
    GameSerializer,
    SingleWordSerializer,
    WordBoxSerializer,
    WordBoxDetailSerializer,
    WordBoxGameEnglishSerializer,
    WordBoxGameInputSerializer,
    WordListSerializer,
    UserListSerializer,
    UserSerializer,
)


# Check word_list and limit length
def word_list_check(items):
    # To prevent duplicated word cast to set
    items = set(items)

    # To prevent too long list
    if len(items) > 100:
        return Response({"detail": "Error! Too long items in list."})

    return items


@api_view()
@permission_classes([permissions.IsAuthenticated])
def login_test_page(request):
    return Response({"detail": "Logged successfully"})


@api_view()
def home(request):
    base_url = "http://127.0.0.1:8000/api/"
    return Response({"detail": "Welcome to home page", "home": base_url})


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated])
def english_list(request):
    if request.method == "GET":
        words = English.objects.all()
        serializer = EnglishSerializer(words, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = EnglishSerializer(data=request.data)
        if serializer.is_valid():
            try:
                English.objects.create(
                    name=serializer.validated_data["name"],
                    word_type=serializer.validated_data.get("word_type"),
                )
            except IntegrityError as e:
                return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
def english_detail(request, word):
    word = get_object_or_404(English, name=word)

    if request.method == "GET":
        serializer = EnglishSerializer(word)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = EnglishSerializer(word, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        if request.user.is_superuser:
            word.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "Error! Only admin can delete"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET", "POST", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
def english_synonyms_list(request, word):
    english = get_object_or_404(English, name=word)

    if request.method == "GET":
        synonyms = english.synonyms.all()
        serializer = EnglishSerializer(synonyms, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = WordListSerializer(data=request.data)
        if serializer.is_valid():
            # Check data length and cat list to set for unique items
            incoming_words = word_list_check(serializer.data["words"])

            # Get or Create Turkish word and english.translations
            for word in incoming_words:
                obj, created = English.objects.get_or_create(
                    name=word,
                )
                english.synonyms.add(obj)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        serializer = WordListSerializer(data=request.data)
        if serializer.is_valid():
            # Check data length and cat list to set for unique items
            incoming_words = word_list_check(serializer.data["words"])
            print(incoming_words)
            # Get synonyms
            words = english.synonyms.filter(name__in=incoming_words)

            # If words is not in list return error
            unknown_words = []
            for word in incoming_words:
                if not words.filter(name=word):
                    unknown_words.append(word)
            if unknown_words:
                return Response(
                    {"detail": "Error", "unknown_words": unknown_words},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Delete selected words from synonyms
            for word in words:
                english.synonyms.remove(word)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
def english_translation_list(request, word):
    english = get_object_or_404(English, name=word)

    if request.method == "GET":
        translations = english.translations.all()
        serializer = TurkishSerializer(translations, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = WordListSerializer(data=request.data)
        if serializer.is_valid():
            # Check data length and cat list to set for unique items
            incoming_words = word_list_check(serializer.data["words"])

            # Get or Create Turkish word and english.translations
            for turkish in incoming_words:
                obj, created = Turkish.objects.get_or_create(
                    name=turkish,
                )
                english.translations.add(obj)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        serializer = WordListSerializer(data=request.data)
        if serializer.is_valid():
            # Check data length and cat list to set for unique items
            incoming_words = word_list_check(serializer.data["words"])

            # Get translations word by name
            words = Turkish.objects.filter(
                translations=english, name__in=incoming_words
            )

            # If words is not in list return error
            unknown_words = []
            for word in incoming_words:
                if not words.filter(name=word):
                    unknown_words.append(word)
            if unknown_words:
                return Response(
                    {"detail": "Error", "unknown_words": unknown_words},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Delete selected words from WordBox
            for word in words:
                english.translations.remove(word)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def game_list(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)


@api_view(["GET"])
# @permission_classes([permissions.IsAuthenticated])
def single_word_detail(request):
    """
    Info page for single word game
    """
    return Response(
        {
            "detail": "Welcome to 'single-word' game. Start to game use link on start key->",
            # "start1": "http://127.0.0.1:8000/" + reverse("single-word-game"),
            "start": request.build_absolute_uri(reverse("api:single-word-start")),
        }
    )


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated])
def single_word_start(request):
    """
    Return a random English word for game
    """

    if request.method == "GET":
        word = English.objects.order_by("?").first()
        return Response({"english": word.name})

    elif request.method == "POST":
        serializer = SingleWordSerializer(data=request.data)
        if serializer.is_valid():
            english = serializer.validated_data["english"]
            translation = serializer.validated_data["turkish"]
            english = get_object_or_404(English, name=english)

            obj, created = SingleWordGame.objects.update_or_create(
                owner=request.user,
                english=english,
                defaults={"answer_status": english.check_translation(translation)},
            )
            # Increase number of play
            obj.increase_number_of_play()
            # Get all translation for feedback
            translations = []
            for i in english.translations.only("name"):
                translations.append(i.name)

            # Choose different word so exclude answered english word
            word = English.objects.order_by("?").exclude(name=english).first()

            return Response(
                {
                    "detail": obj.answer_status,
                    "translations": translations,
                    "english": word.name,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated])
def wordbox_list(request):
    if request.method == "GET":
        own_wordboxes = WordBox.objects.filter(owner=request.user)
        friend_wordboxes = WordBox.objects.filter(users=request.user)
        own_serializer = WordBoxSerializer(own_wordboxes, many=True)
        friend_serializer = WordBoxSerializer(friend_wordboxes, many=True)
        return Response(
            {
                "personal": own_serializer.data,
                "friend": friend_serializer.data,
            }
        )

    elif request.method == "POST":
        serializer = WordBoxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["owner"] = request.user
            try:
                # If you want to use serializer.save() you have to write new serializer
                # because WordBoxSerializer is too general and accept all fields.
                WordBox.objects.create(
                    name=serializer.validated_data["name"], owner=request.user
                )
            except IntegrityError as e:
                return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
def wordbox_detail(request, pk):
    wordbox = get_object_or_404(WordBox, pk=pk)

    if request.method == "GET":
        wordboxdetail = WordBoxDetail.objects.filter(wordbox=wordbox)
        wb_serializer = WordBoxSerializer(wordbox)
        wbd_serializer = WordBoxDetailSerializer(wordboxdetail, many=True)
        data = {
            "wordbox": wb_serializer.data,
            "wordboxdetail": wbd_serializer.data,
            "start": request.build_absolute_uri(
                reverse("api:wordbox-start", args=(pk,))
            ),
        }
        return Response(data)

    # Only name updated (Serializer will be change)
    elif request.method == "PUT":
        serializer = WordBoxSerializer(wordbox, data=request.data)
        if serializer.is_valid():
            wordbox.name = serializer.validated_data["name"]
            wordbox.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        if request.user == wordbox.owner:
            wordbox.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "Error! You must be owner of WordBox to delete"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated])
def wordbox_start(request, pk):
    wordbox = get_object_or_404(WordBox, pk=pk)

    if request.method == "GET":
        if request.session.get("wordbox_has_started", False):
            try:
                word = request.session["words"][-1]
            except IndexError:
                del request.session["wordbox_has_started"]
                del request.session["words"]
                del request.session["words_answered"]
                return Response({"detail": "All questions were answered."})
            return Response({"english": word["name"]})
        else:
            # Set session
            words = wordbox.words.all()
            serializer = WordBoxGameEnglishSerializer(words, many=True)
            request.session["wordbox_has_started"] = True
            # word = {"id": int, "name": str, "translations"=[{"id": int, "name": str}, ...]}
            request.session["words"] = serializer.data
            request.session["words_answered"] = []
            return Response(
                {
                    "detail": "The game has been stared...",
                    "english": request.session["words"][-1]["name"],
                }
            )

    if request.method == "POST":
        # Check session has started
        if request.session.get("wordbox_has_started"):
            # check serializer is_valid()
            serializer = WordBoxGameInputSerializer(data=request.data)
            if serializer.is_valid():
                turkish = serializer.validated_data["turkish"]
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # check request.session["words"].pop() exist
            try:
                word = request.session["words"].pop()
            except IndexError:
                # Delete all game session will be here
                return Response(
                    {"detail": "There is no question for answer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Populate session with value
            answer_status = False
            for translation in word["translations"]:
                if translation["name"] == turkish:
                    answer_status = True
                    break

            word["answer_status"] = answer_status
            request.session["words_answered"].append(word)
            request.session.save()  # Because word is reference to heap

            # check next question is exist
            try:
                next_word = request.session["words"][-1]
            except IndexError:
                for word in request.session["words_answered"]:
                    obj, created = WordBoxDetail.objects.update_or_create(
                        wordbox=wordbox,
                        english_id=word["id"],
                        user=request.user,
                        defaults={"answer_status": word["answer_status"]},
                    )

                # Calculate results and delete session variables
                total = len(request.session["words_answered"])
                correct = 0
                for word in request.session["words_answered"]:
                    if word["answer_status"]:
                        correct += 1

                wrong = total - correct
                result = {"total": total, "correct": correct, "wrong": wrong}

                # Delete session variable for game
                del request.session["wordbox_has_started"]
                del request.session["words"]
                del request.session["words_answered"]

                return Response(
                    {"detail": "Congratulations You've finished the game."} | result
                )

            # Show next question and answer status
            return Response(
                {
                    "detail": f"Answer is {answer_status}",
                    "english": next_word["name"],
                }
            )
        else:
            return redirect("api:wordbox-start", pk)
            return Response(
                {
                    "detail": "First you have to choose your wordbox. To start go to start page",
                    "start": request.build_absolute_uri(reverse("api:wordbox-list")),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["GET", "POST", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
def wordbox_word_list(request, pk):
    wordbox = get_object_or_404(WordBox, pk=pk)

    if request.method == "GET":
        words = wordbox.words.all()
        serializer = EnglishSerializer(words, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = WordListSerializer(data=request.data)
        if serializer.is_valid():
            # Check data length and cat list to set for unique items
            incoming_words = word_list_check(serializer.data["words"])

            # Get word list by name in the list
            words = English.objects.filter(name__in=incoming_words)
            unknown_words = []
            for word in incoming_words:
                if not words.filter(name=word):
                    unknown_words.append(word)
            if unknown_words:
                return Response(
                    {"detail": "Error", "unknown_words": unknown_words},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Add words to WordBox
            for word in words:
                wordbox.words.add(word)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        serializer = WordListSerializer(data=request.data)
        if serializer.is_valid():
            # Check data length and cat list to set for unique items
            incoming_words = word_list_check(serializer.data["words"])

            # Get words in WordBox
            words = English.objects.filter(wordbox=wordbox, name__in=incoming_words)
            unknown_words = []
            for word in incoming_words:
                if not words.filter(name=word):
                    unknown_words.append(word)
            if unknown_words:
                return Response(
                    {"detail": "Error", "unknown_words": unknown_words},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Delete selected words from WordBox
            for word in words:
                wordbox.words.remove(word)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
def wordbox_user_list(request, pk):
    wordbox = get_object_or_404(WordBox, pk=pk)

    if request.method == "GET":
        users = wordbox.users.all()
        print(users)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = UserListSerializer(data=request.data)

        if serializer.is_valid():
            # Check data length and cat list to set for unique items
            incoming_users = word_list_check(serializer.data["users"])

            # Get user list by name in the list
            users = get_user_model().objects.filter(username__in=incoming_users)

            unknown_users = []
            for user in incoming_users:
                if not users.filter(username=user):
                    unknown_users.append(user)
            if unknown_users:
                return Response(
                    {"detail": "Error", "unknown_users": unknown_users},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Add words to WordBox
            for user in users:
                wordbox.users.add(user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        serializer = UserListSerializer(data=request.data)
        if serializer.is_valid():
            # Check data length and cat list to set for unique items
            incoming_users = word_list_check(serializer.data["users"])

            # Get user list by name in the list
            users = wordbox.users.filter(username__in=incoming_users)

            unknown_users = []
            for user in incoming_users:
                if not users.filter(username=user):
                    unknown_users.append(user)

            if unknown_users:
                return Response(
                    {"detail": "Error", "unknown_users": unknown_users},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Delete selected words from WordBox
            for user in users:
                wordbox.users.remove(user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
