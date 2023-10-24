# Generated by Django 4.2.6 on 2023-10-24 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore_app', '0013_alter_book_user_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='dislikes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]