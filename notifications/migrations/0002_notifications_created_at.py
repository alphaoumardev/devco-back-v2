# Generated by Django 4.1.2 on 2022-11-19 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
