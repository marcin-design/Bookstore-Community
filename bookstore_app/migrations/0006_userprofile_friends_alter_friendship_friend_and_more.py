# Generated by Django 4.2.6 on 2023-10-21 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore_app', '0005_remove_userprofile_last_saved_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(through='bookstore_app.Friendship', to='bookstore_app.userprofile'),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookstore_app.userprofile'),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_friendships', to='bookstore_app.userprofile'),
        ),
    ]
