# Generated by Django 3.2.8 on 2021-11-11 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='skitte-images/post/%Y/%m/', verbose_name='Image')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='skit',
            name='image',
        ),
        migrations.AddField(
            model_name='skit',
            name='image',
            field=models.ManyToManyField(blank=True, to='skit.Image'),
        ),
    ]