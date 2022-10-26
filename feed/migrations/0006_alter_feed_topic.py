# Generated by Django 4.1.2 on 2022-10-24 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0002_alter_topics_name'),
        ('feed', '0005_rename_user_feed_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topic', to='topics.topics'),
        ),
    ]
