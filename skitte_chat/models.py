from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import pre_save
from skitte.utils import chat_unique_slug_generator
from profiles.models import Profile
from django.utils.translation import gettext_lazy as _
from skitte.utils import image_resize

User = settings.AUTH_USER_MODEL


class PublicChatRoom(models.Model):
    title = models.CharField(max_length=150, blank=False)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        _("Image"), upload_to="skitte-images/group/%Y/%m/", blank=True, null=True)
    slug = models.SlugField(max_length=50, null=False, blank=False)
    created_by = models.ForeignKey(
        User, related_name="room_created_by", on_delete=models.CASCADE)
    users = models.ManyToManyField(
        User, blank=True, related_name='chats', help_text="user who are online")
    admins = models.ManyToManyField(
        User, blank=True, help_text="user who are admin", related_name="room_admin")
    messages = models.ManyToManyField("PublicRoomChatMessage", blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title}@{self.pk}"

    def save(self, *args, **kwargs):
        # run save of parent class above to save original image to disk
        super().save(*args, **kwargs)

        if self.image:
            image_resize(self.image, 80, 80)

    def connect_user(self, user):
        """
        Return True is user is added to the users list
        """
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.user.all():
            is_user_added = True
        return is_user_added

    def disconnect_user(self, user):
        """
        Return True is user is removed to the users list
        """
        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed

    def check_if_user_is_from_room(self, slug, user):
        qs = self.objects.filter(slug=slug).first()
        if user in qs.users.all():
            return True
        else:
            return False

    @property
    def group_name(self):
        """
        Return the channels group name that sockets should subscribe to 
        and get sent msg as they are generated.
        """
        return f"PublicChatRoom-{self.id}"


class PublicRoomChatMessageManager(models.Model):
    def by_room(self, pk):
        qs = PublicRoomChatMessageManager.objects.filter(
            id=pk).order_by("-timestamp")
        return qs


class PublicRoomChatMessage(models.Model):
    """
    Chat message created by a user inside a PublicChatRoom (foreign Key)
    """
    user = models.ForeignKey(
        Profile, related_name='messages', on_delete=models.CASCADE)
    room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PublicRoomChatMessageManager()

    def __str__(self):
        return self.content

    def last_10_messages(self):
        return PublicRoomChatMessage.objects.order_by('-timestamp').all()[:10]


class PrivateThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='+')
    slug = models.SlugField(max_length=50, unique=True, null=False, blank=False)
    messages = models.ManyToManyField("PublicRoomChatMessage", blank=True)
    timestamp = models.DateTimeField(default=timezone.now)


class PrivateMessageModel(models.Model):
    thread = models.ForeignKey(
        "PrivateThreadModel", related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='+')
    body = models.TextField()
    image = models.ImageField(
        upload_to='images/message_photos', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def last_10_messages(self):
        return PrivateMessageModel.objects.order_by('-timestamp').all()[:10]


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = chat_unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender=PublicChatRoom)
pre_save.connect(pre_save_receiver, sender=PrivateThreadModel)
