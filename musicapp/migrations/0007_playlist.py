# Generated by Django 3.2 on 2021-04-19 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0006_songs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist_name', models.CharField(max_length=200)),
            ],
        ),
    ]
