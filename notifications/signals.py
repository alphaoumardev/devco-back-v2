from django.db.models.signals import post_save, pre_save, post_delete, pre_delete

from feed.models import Feed, Comments
from notifications.models import Notifications


def new_feed_created(sender, instance, created, **kwargs):
    if not created:
        return
    my_followers = instance.profiles.followers.all()
    for follower in my_followers:
        Notifications.objects.create(
            to_profile=follower,
            from_profile=instance.profiles,
            notification_type='new_post',
            new_post=instance,
            content=f"{instance.profiles.user.username} has posted an new Article"
        )


def new_comment_created(sender, instance, created, **kwargs):
    if not created:
        return
    my_followers = instance.profiles.followers.all()
    for follower in my_followers:
        Notifications.objects.create(
            to_profile=follower,
            from_profile=instance.profiles,
            notification_type='new_post',
            new_post=instance,
            content=f"{instance.profiles.user.username} has posted an new Article"
        )


post_save.connect(new_feed_created, sender=Feed)

post_save.connect(new_feed_created, sender=Feed)
