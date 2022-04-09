from django.contrib import admin

from .models import Document, Chapter, Textz, PassCode as Pass

admin.site.register(Document)
admin.site.register(Chapter)
admin.site.register(Textz)
admin.site.register(Pass)