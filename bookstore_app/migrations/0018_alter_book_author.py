# Generated by Django 4.2.6 on 2023-10-28 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore_app', '0017_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=250),
        ),
    ]
