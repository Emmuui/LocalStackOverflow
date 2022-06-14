from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Vote


@receiver(pre_save, sender=Vote)
def vote_pre_save_signal(sender, instance, **kwargs):

    if instance.id:
        current = instance
        print(f'New rating =  {current.choose_rating}')
        previous = Vote.objects.get(id=instance.id)
        print(f'Previous rating = {previous.choose_rating}')
        if previous.choose_rating != current.choose_rating:
            if previous.choose_rating == str(0):
                instance.choose_rating = current.choose_rating
            else:
                instance.choose_rating = 0