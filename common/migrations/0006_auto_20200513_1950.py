# Generated by Django 2.0.13 on 2020-05-13 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20200511_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='access_token',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='facebook_id',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='facebook_profile_url',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='google_access_token',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]