# Generated by Django 4.1.2 on 2022-11-15 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0011_remove_comments_reply_comments_parent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='commentated',
            new_name='timestamp',
        ),
    ]