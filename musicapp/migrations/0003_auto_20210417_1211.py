# Generated by Django 3.2 on 2021-04-17 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0002_users_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
