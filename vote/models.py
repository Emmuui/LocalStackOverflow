from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from userapp.models import UserProfile


class Vote(models.Model):
    """ Vote for question or answer """
    rating_choice = (
        ('1', 1),
        ('0', 0),
        ('-1', -1)
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    choose_rating = models.CharField(max_length=50, choices=rating_choice)
    created_at = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(
        verbose_name='related object',
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.id} - {self.user} - {self.choose_rating}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)