from userapp.models import UserProfile, Rank
from .models import Question


def add_rating_to_user(instance):
    """ Add rating to user each time
     when user create an answer or a question """
    ranks = Rank.objects.all()
    user = UserProfile.objects.get(pk=instance.id)
    user.rating += 450
    if user.rating <= 100:
        user.rank = ranks.get(name='Beginner')
    elif 101 <= user.rating <= 500:
        user.rank = ranks.get(name='Confident user')
    elif 501 <= user.rating <= 3000:
        user.rank = ranks.get(name='Pro')
    user.save()
    return user

