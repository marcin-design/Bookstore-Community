# Generated by Django 4.2.6 on 2023-10-25 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore_app', '0014_book_dislikes_book_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='liked',
            field=models.BooleanField(default=False),
        ),
    ]
