# Generated by Django 3.2.8 on 2021-11-26 22:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('skitte_chat', '0003_publicchatroom_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicchatroom',
            name='users',
            field=models.ManyToManyField(blank=True, help_text='user who are online', related_name='chats', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
    ]