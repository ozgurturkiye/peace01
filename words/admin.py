from django.contrib import admin

from .models import Turkish, English, SingleWordGame, WordBox, WordBoxDetail


admin.site.register(Turkish)
admin.site.register(English)
admin.site.register(SingleWordGame)
admin.site.register(WordBox)
admin.site.register(WordBoxDetail)
