from django.contrib import admin
from .models import PrivateThreadModel, PublicChatRoom, PublicRoomChatMessage

admin.site.register(PublicChatRoom)
admin.site.register(PrivateThreadModel)
admin.site.register(PublicRoomChatMessage)
