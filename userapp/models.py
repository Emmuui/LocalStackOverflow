from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """ User with AbstractUser """

    avatart = models.ImageField()
    description = models.TextField(max_length=2000, null=True, blank=True)
    rating = models.SmallIntegerField(null=True, blank=True)
    rank = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)



