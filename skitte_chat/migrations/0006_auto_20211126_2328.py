# Generated by Django 3.2.8 on 2021-11-26 22:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('skitte_chat', '0005_alter_publicchatroom_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicchatroom',
            name='users',
            field=models.ManyToManyField(blank=True, help_text='user who are online', related_name='chats', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='publicroomchatmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='profiles.profile'),
        ),
    ]
