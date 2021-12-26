from rest_framework import serializers

from ..models import PublicChatRoom, PrivateThreadModel
from ..views import get_user_contact


class ContactSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class PublicChatRoomSerializer(serializers.ModelSerializer):
    users = ContactSerializer(many=True)

    class Meta:
        model = PublicChatRoom
        fields = ('id', 'image', 'messages', 'users', 'title', 'timestamp')
        read_only = ('id')

    def create(self, validated_data):
        print(validated_data)
        participants = validated_data.pop('users')
        chat = PublicChatRoom()
        chat.save()
        for username in participants:
            contact = get_user_contact(username)
            chat.participants.add(contact)
        chat.save()
        return chat


class PrivateChatRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrivateThreadModel
        fields = ('id', 'user', 'receiver', 'messages', 'timestamp')
        read_only = ('id')



# do in python shell to see how to serialize data

# from chat.models import Chat
# from chat.api.serializers import ChatSerializer
# chat = Chat.objects.get(id=1)
# s = ChatSerializer(instance=chat)
# s
# s.data
