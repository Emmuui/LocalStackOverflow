from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from userapp.models import UserProfile


class Vote(models.Model):
    """ Vote for question or answer """
    rating_choice = (
        ('UP_VOTE', 1),
        ('DOWN_VOTE', -1)
    )

    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    choose_rating = models.CharField(max_length=50, choices=rating_choice)
    created_at = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, null=True,
                                     blank=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(
        verbose_name='related object',
        null=True,
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.username} - {self.choose_rating}'