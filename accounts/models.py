from django.db import models
from django.contrib.auth.models import AbstractUser


def profile_image_path(instance, filename):
    return f'profile_images/{instance.user.username}/{filename}'


class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    profile_image = models.ImageField(blank=True, upload_to=profile_image_path)