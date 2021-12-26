from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from ..views import get_user_contact
from ..models import PublicChatRoom, PrivateThreadModel
from .serializers import PrivateChatRoomSerializer, PublicChatRoomSerializer

User = get_user_model()


class ChatListView(ListAPIView):
    serializer_class = PublicChatRoomSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        queryset = PublicChatRoom.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            contact = get_user_contact(username)
            queryset = contact.chats.all()
        return queryset


class RoomListView(ListAPIView):
    serializer_class = PrivateChatRoomSerializer
    permission_classes = (permissions.AllowAny, permissions.IsAuthenticated)

    def get_queryset(self):
        username = self.request.user.username
        queryset = PrivateThreadModel.objects.filter(user__username=username)
        if not queryset.exist():
            queryset = PrivateThreadModel.objects.filter(
                reciver__username=username)
        return queryset.all()


class ChatDetailView(RetrieveAPIView):
    queryset = PublicChatRoom.objects.all()
    serializer_class = PublicChatRoomSerializer
    permission_classes = (permissions.AllowAny, )


class ChatCreateView(CreateAPIView):
    queryset = PublicChatRoom.objects.all()
    serializer_class = PublicChatRoomSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChatUpdateView(UpdateAPIView):
    queryset = PublicChatRoom.objects.all()
    serializer_class = PublicChatRoomSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChatDeleteView(DestroyAPIView):
    queryset = PublicChatRoom.objects.all()
    serializer_class = PublicChatRoomSerializer
    permission_classes = (permissions.IsAuthenticated, )
