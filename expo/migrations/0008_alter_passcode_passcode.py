# Generated by Django 3.2 on 2022-04-09 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expo', '0007_alter_passcode_passcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passcode',
            name='passcode',
            field=models.CharField(blank=True, max_length=5, null=True, unique=True),
        ),
    ]