from django.db import models
from topics.models import Topics
from users.models import Profile
from ckeditor.fields import RichTextField


class Feed(models.Model):
    title = models.CharField(max_length=100)
    # content = models.CharField(max_length=10000, null=False)
    content = RichTextField()
    shares = models.IntegerField(null=True, blank=True)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, related_name="topic", null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    posted = models.DateTimeField(auto_now_add=True, null=True)
    cover_image = models.ImageField(upload_to='devcom', null=True, blank=True, )
    likes = models.ManyToManyField(Profile, related_name="related_like", blank=True)
    saves = models.ManyToManyField(Profile, related_name="related_save", blank=True)
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
        return self.comments_set.count()

    @property
    def replies(self):
        return self.comments_set.filter(parent__comment=None)


class Comments(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="subcomments", null=True, blank=True)
    post = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True, blank=True)
    commentator = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, )
    liking = models.ManyToManyField(Profile, related_name="like_reply", blank=True)
    comment = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.comment

    def children(self):  # replies
        return Comments.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    @property
    def like_count(self):
        return self.liking.count()
