from django.db.models.signals import post_save
from django.dispatch import receiver
from question.models import Question, Answer, Comment
from .services import UserRating


@receiver(post_save, sender=Question)
@receiver(post_save, sender=Answer)
@receiver(post_save, sender=Comment)
def add_to_rating(sender, instance, **kwargs):
    if instance:
        one_record = 1
        service = UserRating(user=instance.user, one_record=one_record)
        service.count_user_rating()
