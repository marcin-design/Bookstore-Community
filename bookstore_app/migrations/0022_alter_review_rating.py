# Generated by Django 4.2.6 on 2023-10-31 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore_app', '0021_book_disliked_users_book_liked_users_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(null=True),
        ),
    ]