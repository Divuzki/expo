from .models import Skit
from django.conf import settings
from profiles.serializers import PublicProfileSerializer

from rest_framework import serializers
from rest_framework.response import Response

MAX_SKIT_LENGTH = settings.MAX_SKIT_LENGTH
UPLOAD_URL = settings.URL+settings.MEDIA_URL
SKIT_ACTION_OPTIONS = settings.SKIT_ACTION_OPTIONS


class SkitActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)
    image = serializers.CharField(required=False)
    video = serializers.CharField(required=False)

    def validate_action(self, value):
        value = value.lower().strip()  # "Like " -> "like"
        if not value in SKIT_ACTION_OPTIONS:
            raise serializers.ValidationError(
                "This is not a valid action for skitte")
        return value


class SkitCreateSerializer(serializers.ModelSerializer):
    # serializers.SerializerMethodField(read_only=True)
    user = PublicProfileSerializer(source='user.profile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    reposts = serializers.SerializerMethodField(read_only=True)
    didlike = serializers.SerializerMethodField(read_only=True)
    date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Skit
        fields = [
            'user',
            'id',
            'slug',
            'content',
            'caption',
            'textInImage',
            'image',
            'video',
            'likes',
            'reposts',
            'didlike',
            'date',
            'timestamp']

    def get_date(self, obj):
        months = ["JAN", "FEB", "MARCH", "APR", "MAY",
                  "JUNE", "JULY", "AUG", "SEP", "OCT", "NOV", "DEC"]
        date = f"{months[obj.timestamp.date().month -1]} {obj.timestamp.date().day}"
        return date

    def get_likes(self, obj):
        return obj.likes.count()

    def get_reposts(self, obj):
        qs = Skit.objects.filter(parent_id=obj.id).all()
        qs = qs.count()
        return qs

    def get_didlike(self, obj):
        didlike = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user.username
            didlike = user in obj.likes.all()
        return didlike

    def get_image(self, obj):
        image = None
        if obj.image:
            image = UPLOAD_URL + obj.image
        elif obj.caption:
            image = UPLOAD_URL + obj.caption
        image.replace("https//", "")
        image.replace("sktmedia//", "")
        return image

    def get_video(self, obj):
        if obj.video:
            return UPLOAD_URL + obj.video

    def validate_content(self, value):
        if len(value) > MAX_SKIT_LENGTH:
            return Response({"error": "This skitte is too long"}, status=400)
        return value


class SkitSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    didlike = serializers.SerializerMethodField(read_only=True)
    reposts = serializers.SerializerMethodField(read_only=True)
    parent = SkitCreateSerializer(read_only=True)
    date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Skit
        fields = [
            'user',
            'id',
            'slug',
            'content',
            'caption',
            'textInImage',
            'image',
            'video',
            'likes',
            'reposts',
            'didlike',
            'is_repost',
            'parent',
            'date',
            'timestamp']

    def get_date(self, obj):
        months = ["JAN", "FEB", "MARCH", "APR", "MAY",
                  "JUNE", "JULY", "AUG", "SEP", "OCT", "NOV", "DEC"]
        date = f"{months[obj.timestamp.date().month -1]} {obj.timestamp.date().day}"
        return date

    def get_likes(self, obj):
        return obj.likes.count()

    def get_reposts(self, obj):
        qs = Skit.objects.filter(parent_id=obj.id).all()
        qs = qs.count()
        return qs

    def get_image(self, obj):
        image = None
        if obj.image:
            image = UPLOAD_URL + obj.image
        elif obj.caption:
            image = UPLOAD_URL + obj.caption
        image.replace("https//", "")
        image.replace("sktmedia//", "")
        return image

    def get_didlike(self, obj):
        didlike = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            didlike = user in obj.likes.all()
        return didlike

    def get_video(self, obj):
        if obj.video:
            return UPLOAD_URL + obj.video
