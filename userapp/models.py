from django.db import models
from django.contrib.auth.models import AbstractUser
from .services import upload_file


class UserProfile(AbstractUser):
    """ User with AbstractUser """

    avatar = models.ImageField(upload_to=upload_file)
    description = models.TextField(max_length=2000, null=True, blank=True)
    rating = models.IntegerField(default=100, null=True, blank=True)
    rank = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)




