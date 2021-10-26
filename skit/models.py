import os
import textwrap
from io import BytesIO
from django.db.models import Q
from django.db import models
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

from django.db.models.signals import pre_save
from skitte.utils import unique_slug_generator, image_resize
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage as storage

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

User = settings.AUTH_USER_MODEL
DEBUG = settings.DEBUG


class SkitLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skit = models.ForeignKey("Skit", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class SkitQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)

    def by_location(self, location):
        return self.filter(user__profile__location__iexact=location)

    def feed(self, user):
        profiles_exist = user.following.exists()
        followed_users_id = []
        if profiles_exist:
            followed_users_id = user.following.values_list(
                "user__id", flat=True)  # [x.user.id for x in profiles]
        return self.filter(
            Q(user__id__in=followed_users_id) |
            Q(user=user)
        ).distinct().order_by("-timestamp")


class SkitManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return SkitQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)

    def by_username(self, username):
        return self.get_queryset().by_username(username)

    def by_location(self, location):
        return self.get_queryset().by_location(location)


class Skit(models.Model):
    # Maps to SQL data
    # id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(
        "self", null=True, on_delete=models.SET_NULL)
    # many users can many skits
    slug = models.SlugField(max_length=50, null=True,
                            blank=True)  # create a unique url
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="skits")
    likes = models.ManyToManyField(
        User, related_name='skit_user', blank=True, through=SkitLike)
    content = models.TextField(blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    image = models.ImageField(
        _("Image"), upload_to="images/post/%Y/%m/", blank=True, null=True)
    video = models.FileField(
        _("Video"), upload_to="videos/post/%Y/%m/", blank=True, null=True)
    audio = models.FileField(
        _("Audio"), upload_to="audios/post/%Y/%m/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = SkitManager()

    def get_absolute_url(self):
        slug = f"post/₦/{self.slug}/"
        return slug

    def save(self, *args, **kwargs):
        # run save of parent class above to save original image to disk
        super().save(*args, **kwargs)

        # img.thumbnail(output_size, Image.ANTIALIAS)
        memfile = BytesIO()
        if self.image:
            image_resize(self.image, 500, 460)
        elif not self.image and not self.video and not self.content and self.caption:
            caption = self.caption
            imgpath = f'contentBackgroundImage\\skt_cation\\{self.id}\\skt_cation+{caption}&id+{self.id}16-17-18@{self.user.username}_image.png'
            imgpath = f"{imgpath.replace(' ', '0')}.png"
            wrapper = textwrap.TextWrapper(width=35)
            word_list = wrapper.wrap(text=caption)
            msg = ''

            for ii in word_list[:-1]:
                msg = msg + ii + '\n'
            msg += word_list[-1]

            W, H = (800, 460)
            img = Image.new("RGBA", (W, H), "black")
            draw = ImageDraw.Draw(img)

            # font = ImageFont.truetype(<font-file>, <font-size>)
            font = ImageFont.truetype(os.path.join(
                BASE_DIR, "static/fonts/seguiemj.ttf"), 48, layout_engine=ImageFont.LAYOUT_RAQM)
            w, h = draw.textsize(msg, font=font)
            draw.text(((W - w) / 2, (H-h)/2), msg,
                      fill="#faa", font=font
                      # , embedded_color=True
                      )
            img.save(memfile, 'PNG', quality=95)
            storage.save(imgpath, memfile)
            memfile.close()
            img.close()
            if self.pk is None:
                Skit.objects.update(
                    content='', image=imgpath, caption=self.content)
            self.image = imgpath
            self.content = ''

    class Meta:
        ordering = ['-id']

    @property
    def is_repost(self):
        return self.parent != None


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_user")
    post = models.ForeignKey(
        Skit, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField()
    likes = models.ManyToManyField(
        User, related_name='comment_likes', blank=True, through=CommentLike)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.id, self.user.username)


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender=Skit)
