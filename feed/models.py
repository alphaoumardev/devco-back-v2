from django.contrib.auth.models import User
from django.db import models
from topics.models import Topics


class Feed(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=10000, null=False)
    shares = models.IntegerField(null=True, blank=True)
    topic = models.ForeignKey(Topics, on_delete=models.PROTECT, related_name="topic", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    posted = models.DateTimeField(auto_now_add=True, null=True)
    cover_image = models.ImageField(upload_to='devcom', null=True, blank=True,)
    likes = models.ManyToManyField(User, related_name="related_like", blank=True)
    saves = models.ManyToManyField(User, related_name="related_save", blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def num_likes(self):
        return self.likes.count()

    @property
    def num_saves(self):
        return self.saves.count()

    @property
    def num_replies(self):
        return self.replies_set.count()


class Replies(models.Model):
    post = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=2000)
    like = models.IntegerField(null=True, blank=True)
    commentator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, )
    commentated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-like']
