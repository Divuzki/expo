from django.contrib import admin

from .models import Skit, SkitLike


class SkitLikeAdmin(admin.TabularInline):
        model = SkitLike


class SkitAdmin(admin.ModelAdmin):
    inlines = [SkitLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']
    prepopulated_fields = {"slug": ("content","caption")}
    class Meta:
        model = Skit

admin.site.register(Skit, SkitAdmin)
