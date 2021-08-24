from rest_framework import serializers
from django.http import JsonResponse
from .models import Profile, FriendRequest
from skit.models import Skit
from django.conf import settings
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "is_active"
        ]


class PublicProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    is_friend = serializers.SerializerMethodField(read_only=True)
    is_user = serializers.SerializerMethodField(read_only=True)
    
    friends_list = serializers.SerializerMethodField(read_only=True)

    #new gql
    received_request = serializers.SerializerMethodField(read_only=True)
    sent_request = serializers.SerializerMethodField(read_only=True)

    is_verified = serializers.SerializerMethodField(read_only=True) 
    show_full_name = serializers.SerializerMethodField(read_only=True) 

    username = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)

    follower_count = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    followed_by = serializers.SerializerMethodField(read_only=True)
    post_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "likes",
            "bio",
            "location",
            "website",
            "image",
            "follower_count",
            "following_count",
            "followed_by",
            "is_following",
            "is_friend",
            "is_user",
            "is_verified",
            "show_full_name",
            "received_request",
            "sent_request",
            "friends_list",
            "post_count",
        ]

    def get_post_count(self, obj):
        username = obj.user.username
        qs = Skit.objects.filter(user__username__iexact=username)
        return len(qs)

    def get_followed_by(self, obj):
        followed_by = []
        context = self.context
        request = context.get("request")
        if request:
            if request.user.is_authenticated:
                user = obj.followers.all().values_list("profile__user__username", flat=True)
                me = request.user.following.all().values_list("user__username", flat=True)
                for qs in me:
                    for qt in user:
                        if qs in qt:
                            followed_by.append(qs)
            return followed_by

    def get_is_following(self, obj):
        is_following = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            is_following = user in obj.followers.all()
        return is_following

    def get_likes(self, obj):
        username = obj.user.username
        qs = Skit.objects.filter(user__username__iexact=username)
        if username != None:
            qs_list = []
            qs = qs.values_list("likes", flat=True)
            for qs in qs:
                if not qs == None:
                    qs_list.append(qs)
            return len(qs_list)

    def get_is_user(self, obj):
        is_user = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            if user.username == obj.user.username:
                is_user = True
        return is_user

    def get_image(self, obj):
        # "//"+settings.URL+
        image_link = None
        if obj.image:
            image_link = obj.image
        return obj.image

    def get_friends_list(self, obj):
        friends_list = []
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            if user.username == obj.user.username:
                me = Profile.objects.filter(user=user)
                # req_check = FriendRequest.objects.filter(
                #     from_user=obj.user, to_user=user)
                # req_check1 = FriendRequest.objects.filter(
                #     from_user=user, to_user=obj.user)
                if me:
                    me = Profile.objects.filter(id=obj.user.id)
                    friends_list = me.values_list(
                        "friends__user__username", "friends__image", "friends__id")
                    friends_list = {
                        "count": friends_list.count(),
                        "friends": friends_list
                    }
            return friends_list

    def get_is_friend(self, obj):
        is_friend = "none"
        context = self.context
        request = context.get("request")
        if request:
            p = Profile.objects.filter(user=obj.user).first()
            if request.user.is_authenticated:
                if request.user.profile not in p.friends.all():
                    is_friend = "not_friend"
                    if len(FriendRequest.objects.filter(
                            from_user=request.user).filter(to_user=p.user)) == 1:
                        is_friend = "requested"
                    elif FriendRequest.objects.filter(to_user=request.user, from_user=obj.user).exists():
                        is_friend = "requesting"

        return is_friend

    def get_received_request(self, obj):
        rec_rq = []
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            if user.username == obj.user.username:
                rec_rq = FriendRequest.objects.filter(to_user=obj.user).values_list(
                    "from_user__username", "from_user__profile__image")
                rec_rq = {
                    "count": rec_rq.count(),
                    "requests": rec_rq
                }
            return rec_rq

    def get_sent_request(self, obj):
        sent_rq = []
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            if user.username == obj.user.username:
                sent_rq = FriendRequest.objects.filter(from_user=obj.user).values_list(
                    "to_user__username", "to_user__profile__image")
                sent_rq = {
                    "count": sent_rq.count(),
                    "requests": sent_rq
                }
            return sent_rq

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    def get_is_verified(self, obj):
        return obj.user.is_verified

    def get_show_full_name(self, obj):
        qs = obj.user.is_show_full_name
        if obj.user.first_name and obj.user.first_name is None:
            qs = False
        return qs

    def get_following_count(self, obj):
        return obj.user.following.count()

    def get_follower_count(self, obj):
        return obj.followers.count()
