import random
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import is_safe_url
from ..models import Profile, FriendRequest
from ..serializers import PublicProfileSerializer, UserProfileSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics

User = get_user_model()

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


# DetailView, UpdateView And EditView
class ProfileDetailUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'user__username'  # slug, id | path('<int:pk>\d+')
    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
    lookup_field = 'user__username'  # slug, id | path('<int:pk>\d+')
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def profile_detail_api_view(request, username, *args, **kwargs):
    # Get the profile for past username
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        return Response({"detail": "User Not Found"}, status=404)
    profile_obj = qs.first()
    data = request.data or {}
    if request.method == "POST":
        me = request.user
        user = get_object_or_404(User, username=username)
        action = data.get("action")
        if profile_obj.user != me:
            if action == "follow":
                profile_obj.followers.add(me)
            elif action == "unfollow":
                profile_obj.followers.remove(me)

            # Friend Requests
            elif action == "add friend":
                if not FriendRequest.objects.filter(from_user=me, to_user=user).exists():
                    frequest, created = FriendRequest.objects.get_or_create(
                        from_user=me,
                        to_user=user
                    )
            elif action == "cancel request" or action == "ignore":
                frequest = FriendRequest.objects.filter(
                    from_user=me, to_user=user)
                if action == "ignore" or action == "ignoring":
                    frequest = FriendRequest.objects.filter(
                        from_user=user, to_user=me)

                frequest.delete()

            elif action == "friend":
                from_user = get_object_or_404(User, username=username).id
                from_user = get_object_or_404(User, id=from_user)
                user2 = from_user
                me.profile.friends.remove(user2.profile)
                user2.profile.friends.remove(me.profile)

            elif action == "accept":
                from_user = get_object_or_404(User, username=username).id
                from_user = get_object_or_404(User, id=from_user)
                frequest = FriendRequest.objects.filter(
                    from_user=from_user, to_user=request.user)
                user1 = frequest.first().to_user
                user2 = from_user
                user1.profile.friends.add(user2.profile)
                user2.profile.friends.add(user1.profile)
                frequest.delete()

                # To delete all requests from both sides
                frequest2 = FriendRequest.objects.filter(
                    to_user=from_user, from_user=from_user).all()
                frequest2.delete()
                frequest2 = FriendRequest.objects.filter(
                    to_user=request.user, from_user=request.user).all()
                frequest2.delete()
                frequest2 = FriendRequest.objects.filter(
                    to_user=from_user, from_user=request.user).all()
                frequest2.delete()

            elif action == "accepting":
                to_user = get_object_or_404(User, username=username).id
                to_user = get_object_or_404(User, id=to_user)
                frequest = FriendRequest.objects.filter(
                    to_user=me, from_user=to_user)
                user1 = frequest.first().to_user
                user2 = to_user
                user1.profile.friends.add(user2.profile)
                user2.profile.friends.add(user1.profile)
                frequest.delete()

                # To delete all requests from both sides
                frequest2 = FriendRequest.objects.filter(
                    to_user=to_user, from_user=to_user).all()
                frequest2.delete()
                frequest2 = FriendRequest.objects.filter(
                    to_user=me, from_user=me).all()
                frequest2.delete()
                frequest2 = FriendRequest.objects.filter(
                    to_user=to_user, from_user=me).all()
                frequest2.delete()

            else:
                pass
        else:
            Response({"detail": "Access Denied"}, status=403)
    serializer = PublicProfileSerializer(
        instance=profile_obj, context={"request": request})
    return Response(serializer.data, status=200)
