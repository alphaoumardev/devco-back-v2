from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Devcom  password reset Notice"),
        # message:
        email_plaintext_message,
        # from:
        "devalphaoumar@gmail.com",
        # to:
        [reset_password_token.user.email]
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    avatar = models.ImageField(upload_to="devcom", blank=True, default="https://res.cloudinary.com/diallo/image/upload/v1647154137/8_fncc3c.jpg")
    cover_image = models.ImageField(upload_to="devcom", blank=True, default="https://res.cloudinary.com/diallo/image/upload/v1647154140/4-big_sd6hps.jpg")
    bio = models.TextField(blank=True)
    following = models.ManyToManyField('self', blank=True, symmetrical=False)
    followedby = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="followed_by")

    @property
    def my_posts(self):
        return self.feed_set.all()

    @property
    def my_posts_count(self):
        return self.feed_set.count()

    @property
    def followedby_count(self):
        return self.followedby.count()

    @property
    def follow_count(self):
        return self.following.count()

    def __str__(self):
        return self.user.username

# post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)
