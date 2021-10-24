from django.contrib import admin

from .models import Skit, SkitLike, Comment, CommentLike


class SkitLikeAdmin(admin.TabularInline):
        model = SkitLike


class SkitAdmin(admin.ModelAdmin):
    inlines = [SkitLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']
    prepopulated_fields = {"slug": ("content","caption")}
    class Meta:
        model = Skit

# Comment Like Admin Class
class CommentLikeAdmin(admin.TabularInline):
        model = CommentLike


# Comment Admin Class
class CommentAdmin(admin.ModelAdmin):
    # Inlining CommentLikesAdmin Into CommentAdmin 
    inlines = [CommentLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['post__content', 'post__caption', 'user__username', 'post__user__username']
    class Meta:
        model = Comment

admin.site.register(Skit, SkitAdmin)
admin.site.register(Comment, CommentAdmin)
