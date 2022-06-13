from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from question.models import Question, Answer, Comment
from .models import Vote


@receiver(pre_save, sender=Vote)
def vote_pre_save_signal(sender, instance, **kwargs):
    if instance.id is None:
        pass
    else:
        current = instance
        print(f'New rating =  {current.choose_rating}')
        previous = Vote.objects.get(id=instance.id)
        print(f'Previous rating = {previous.choose_rating}')
        if previous.choose_rating != current.choose_rating:
            if previous.choose_rating == str(0):
                instance.choose_rating = current.choose_rating
            else:
                instance.choose_rating = 0


@receiver(post_save, sender=Vote)
def count_rating(sender, instance, **kwargs):
    model = instance.content_type.model
    if model == 'answer':
        model = Answer.objects.get(pk=instance.object_id)
    elif model == 'comment':
        model = Comment.objects.get(pk=instance.object_id)
    else:
        model = Question.objects.get(pk=instance.object_id)
    positive_rating = model.voting.filter(choose_rating=1).count()
    negative_rating = model.voting.filter(choose_rating=-1).count()
    model.vote_count = positive_rating + (negative_rating * -1)
    print(model.vote_count)
    print(f'Current record = {model}')


