from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

UserModel = settings.AUTH_USER_MODEL


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('You need a username to identify yourself')

        now = timezone.now()
        email = self.normalize_email(email)
        username = username.lower()
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        username = username.lower()
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        username = username.lower()
        user = self._create_user(username, email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        _("first name"), max_length=100, null=True, blank=True, help_text='Enter your name')
    last_name = models.CharField(
        _("last name"), max_length=100, null=True, blank=True, help_text='Enter your surname')
    username = models.CharField(
        _("username"), max_length=50, unique=True, help_text='your username must be unique. It will be public')
    email = models.EmailField(
        _("email"), max_length=254, help_text='E.g example@example.com')
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_show_full_name = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD =  "username"
    EMAIL_FIELD =  "email", 
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    objects = UserManager()

    def get_absolute_url(self):
        return "/profiles/%i/" % (self.username)

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

# -----I will explain this part later. So let's keep it commented for now-------

# class user_type(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     is_teach = models.BooleanField(default=False)
#     is_student = models.BooleanField(default=False)

#     def __str__(self):
#         if self.is_student == True:
#             return User.get_email(self.user) + " - is_student"
#         else:
#             return User.get_email(self.user) + " - is_teacher"
