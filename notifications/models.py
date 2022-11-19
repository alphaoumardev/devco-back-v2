from django.db import models
from users.models import Profile
from feed.models import Feed, Comments


class Notifications(models.Model):
    CHOICES = (("new_follower", "new_follower"), ("new_comment", "new_comment"), ("new_post", "new_post"))
    content = models.CharField(max_length=200, null=True, blank=True)
    from_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="to_noti")
    to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="from_to")
    notification_type = models.CharField(choices=CHOICES, max_length=18)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    new_post = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True, blank=True)
    new_follower = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.content
