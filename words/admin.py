from django.contrib import admin

from .models import Turkish, English, SingleWordGame, WordBox, WordBoxDetail, Game


class SingleWordGameAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "owner",
        "english",
        "answer_status",
        "updated_at",
        "number_of_play",
    ]


class WordBoxAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "owner",
        "created_at",
        "get_users",
    ]


class WordBoxDetailAdmin(admin.ModelAdmin):
    @admin.display
    def owner(self, obj):
        return obj.wordbox.owner

    list_display = [
        "id",
        "owner",
        "wordbox",
        "english",
        "user",
        "answer_status",
        "updated_at",
    ]


admin.site.register(Turkish)
admin.site.register(English)
admin.site.register(SingleWordGame, SingleWordGameAdmin)
admin.site.register(WordBox, WordBoxAdmin)
admin.site.register(WordBoxDetail, WordBoxDetailAdmin)
admin.site.register(Game)
