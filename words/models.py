from django.conf import settings
from django.db import models
from django.db.models import F


class Turkish(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class English(models.Model):
    WORD_TYPE = [
        ("A", "Adjective"),
        ("N", "Noun"),
        ("V", "Verb"),
    ]
    name = models.CharField(max_length=50, unique=True)
    synonyms = models.ManyToManyField("self", blank=True)
    translations = models.ManyToManyField(
        Turkish, blank=True, related_name="translations"
    )
    word_type = models.CharField(max_length=1, choices=WORD_TYPE, blank=True, null=True)

    def check_translation(self, value) -> bool:
        """Check value is in translations"""
        if self.translations.filter(name__iexact=value).exists():
            return True

        return False

    def __str__(self):
        return self.name


class SingleWordGame(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    english = models.ForeignKey(English, on_delete=models.CASCADE)
    answer_status = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    number_of_play = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "english"], name="unique_owner_english"
            )
        ]

    def increase_number_of_play(self):
        """Avoiding race conditions using F() expression"""
        self.number_of_play = F("number_of_play") + 1
        self.save()

    def __str__(self):
        return f"{self.owner} -> {self.english}"


class WordBox(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    words = models.ManyToManyField(English, blank=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="friends_wb"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "owner"], name="unique_wb_name_owner"
            )
        ]

    def __str__(self):
        return f"{self.name}"

    def get_users(self):
        return ", ".join([i.username for i in self.users.all()])


class WordBoxDetail(models.Model):
    wordbox = models.ForeignKey(WordBox, on_delete=models.CASCADE)
    english = models.ForeignKey(English, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    answer_status = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["wordbox", "user", "english"],
                name="unique_wbd_wordbox_user_english",
            )
        ]

    def __str__(self):
        return f"{self.wordbox} -> {self.wordbox.owner}:{self.user} -> {self.english}"


class Game(models.Model):
    """
    Stores game names.
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
