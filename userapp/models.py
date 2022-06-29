from django.db import models
from django.contrib.auth.models import AbstractUser
from .services import upload_file


class UserProfile(AbstractUser):
    """ User with AbstractUser """

    NEW = 'NEW'
    MIDL = 'MIDL'
    PRO = 'PRO'
    STAFF = 'STAFF'

    CHOICE_RANK = (
        (NEW, 'New'),
        (MIDL, 'Midl'),
        (PRO, 'Pro'),
        (STAFF, 'Staff')
    )

    avatar = models.ImageField(upload_to=upload_file, null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    rating = models.IntegerField(default=10, null=True, blank=True)
    rank = models.CharField(max_length=40, choices=CHOICE_RANK, default=NEW)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-updated_at']
