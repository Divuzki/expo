# Generated by Django 3.2.8 on 2021-11-16 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skit', '0002_auto_20211111_2210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skit',
            name='image',
        ),
        migrations.AddField(
            model_name='skit',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='skit.image'),
        ),
    ]