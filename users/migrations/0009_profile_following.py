# Generated by Django 4.1.2 on 2022-11-10 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_profile_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, to='users.profile'),
        ),
    ]
