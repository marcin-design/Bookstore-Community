# Generated by Django 4.2.6 on 2023-10-19 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore_app', '0003_userprofile_user_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_saved_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]