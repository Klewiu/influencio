# Generated by Django 3.2.8 on 2022-08-04 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_movie_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='video',
        ),
    ]
