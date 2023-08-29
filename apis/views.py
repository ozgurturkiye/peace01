from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from words.models import English, Game, SingleWordGame, WordBox, WordBoxDetail
from .serializers import (
    EnglishSerializer,
    GameSerializer,
    SingleWordSerializer,
    WordBoxSerializer,
    WordBoxDetailSerializer,
    WordBoxGameEnglishSerializer,
    WordBoxGameInputSerializer,
)


@api_view()
def home(request):
    base_url = "http://127.0.0.1:8000/api/"
    return Response({"detail": "Welcome to home page", "home": base_url})


@api_view(["GET", "POST"])
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
                    word_type=serializer.validated_data["word_type"],
                )
            except IntegrityError as e:
                return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
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

            # Choose different word so exclude answered english word
            word = English.objects.order_by("?").exclude(name=english).first()

            return Response(
                {
                    "detail": obj.answer_status,
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
            return Response(
                {
                    "detail": "First you have to choose your wordbox. To start go to start page",
                    "start": request.build_absolute_uri(reverse("api:wordbox-list")),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
