from django.core.exceptions import ValidationError
from question.models import Question, Answer, Comment
from vote.models import Vote


class CountSystem:

    def __init__(self, user, serializer, data):
        self.content_type = data['content_type']
        self.obj_id = data['object_id']
        self.model = {
            'question': Question,
            'answer': Answer,
            'comment': Comment
        }
        self.data = data
        print(f'DATA = {data}')
        self.serializer = serializer
        self.user = user
        self.obj = self.model[self.content_type].objects.get(pk=self.obj_id)

    def update_vote(self):
        print(f'vote id = {self.obj.voting}')

    def validate_user(self):
        values = self.obj.voting.values_list('user', flat=True)
        if self.user.id in values:
            # self.update_vote()
            raise ValidationError('You have already voted')
        else:
            if self.serializer.is_valid():
                self.serializer.save(user=self.user)
                self.count_vote()
            return self.serializer

    def count_vote(self):
        positive_rating = self.obj.voting.filter(choose_rating=1).count()
        negative_rating = self.obj.voting.filter(choose_rating=-1).count()
        print(f'negative = {negative_rating}, positive = {positive_rating}')
        self.obj.vote_count = (positive_rating + (negative_rating * -1))
        self.obj.save()
        return self.obj

    def run_system(self):
        self.validate_user()


class UserRating:

    def __init__(self, user):
        self.user = user
        self.mult_by = 10
        self.local_rating = 0

    def count_user_rating(self):
        question = Question.objects.filter(user=self.user.id).count()
        answer = Answer.objects.filter(user=self.user.id).count()
        comment = Comment.objects.filter(user=self.user.id).count()
        self.local_rating = self.mult_by * (question + answer + comment)
        # self.user.rating = self.local_rating + self.obj.vote_count + 50

        if self.user.rating <= 100:
            self.user.rank = 'NEW'
        elif 100 < self.user.rating <= 200:
            self.user.rank = 'MIDL'
        elif 300 < self.user.rating < 400:
            self.user.rank = 'MIDL'
        elif 400 < self.user.rating <= 500:
            self.user.rank = 'PRO'
        elif self.user.rating > 500:
            self.user.is_staff = True
        self.user.save()
        return self.user


def one_time_add(user):
    user.rating += 10
    user.save()
    return user


def validate_time_create():
    pass
