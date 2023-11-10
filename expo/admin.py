from django.contrib import admin

from .models import Document, Chapter, Question, Passcode

admin.site.register(Document)
admin.site.register(Chapter)
admin.site.register(Question)
admin.site.register(Passcode)