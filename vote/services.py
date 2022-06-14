from django.core.exceptions import ValidationError

from question.models import Question, Answer, Comment
from userapp.models import Rank


class CountSystem:

    def __init__(self, content_type, obj_id, user):
        self.content_type = content_type
        self.obj_id = obj_id
        self.model = {
            'question': Question,
            'answer': Answer,
            'comment': Comment
        }
        self.local_rating = 0
        if self.content_type and self.obj_id is not None:
            self.obj = self.model[self.content_type].objects.get(pk=self.obj_id)
        self.user = user
        self.query_rank = Rank.objects.all().values_list('name', flat=True)

    def validate_user(self):
        values = self.obj.voting.values_list('user', flat=True)
        if self.user.id in values:
            raise ValidationError('You have already voted')

    def count_vote(self):
        positive_rating = self.obj.voting.filter(choose_rating=1).count()
        negative_rating = self.obj.voting.filter(choose_rating=-1).count()
        print(f'negative = {negative_rating}, positive = {positive_rating}')
        self.obj.vote_count = (positive_rating + (negative_rating * -1))
        self.obj.save()
        self.count_user_rating()
        return self.obj

    def count_user_rating(self):
        question = Question.objects.filter(user=self.user.id).count()
        answer = Answer.objects.filter(user=self.user.id).count()
        comment = Comment.objects.filter(user=self.user.id).count()
        self.local_rating = 10 * (question + answer + comment)
        self.user.rating = self.local_rating + self.obj.vote_count
        self.user.save()
        return self.user













