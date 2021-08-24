from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.db import models
from PIL import Image

from django.core.files.storage import default_storage as storage
from io import BytesIO

User = settings.AUTH_USER_MODEL


class FollowerRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        _("Image"), upload_to="images/profile/%Y/%m/", default="profile-image-placeholder.png")
    location = models.CharField(max_length=20, default="Earth")
    bio = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    website = models.CharField(max_length=150, null=True, blank=True)
    followers = models.ManyToManyField(
        User, related_name='following', blank=True)  # WHY Following in related_name
    friends = models.ManyToManyField(
        "Profile", related_name='friend', blank=True)
    """
    project_obj = Profile.objects.first()
    project_obj = followers.all() -> All users following this profile
    user.following.all() -> All user profiles I follow
    """

    def __str__(self):
        return f"{self.user.username} stays in {self.location}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        memfile = BytesIO()

        if self.image:
            img = Image.open(self.image)
            if img.height > 180 or img.width > 180:
                output_size = (180, 180)
                img.thumbnail(output_size, Image.ANTIALIAS)
                img.save(memfile, 'JPEG', quality=95)
                storage.save(self.image.name, memfile)
                memfile.close()
                img.close()


class FriendRequest(models.Model):
    to_user = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "From {}, To {} ".format(self.from_user.username, self.to_user.username)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()
