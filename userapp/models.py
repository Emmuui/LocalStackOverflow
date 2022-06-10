from django.db import models
from django.contrib.auth.models import AbstractUser
from .services import upload_file


class Rank(models.Model):
    name = models.CharField(max_length=150, verbose_name='Name of rank')

    def __str__(self):
        return f'{self.id} - {self.name}'

    class Meta:
        verbose_name_plural = 'Ranks'
        verbose_name = 'Rank'


class UserProfile(AbstractUser):
    """ User with AbstractUser """

    avatar = models.ImageField(upload_to=upload_file, null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    rating = models.IntegerField(default=10, null=True, blank=True)
    rank = models.ForeignKey(Rank, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-updated_at']
