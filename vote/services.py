from question.models import Question, Answer, Comment
from vote.models import Vote
from rest_framework.response import Response
from rest_framework import status, serializers
import datetime


class CountSystem:

    def __init__(self, user, data):
        self.content_object = data['content_object']
        self.data = data
        self.user = user
        self.vote = 0

    def update_vote(self):
        next_vote = self.data['choose_rating']
        previous_vote = self.content_object.voting.get(user=self.user)
        if previous_vote.choose_rating != next_vote:
            if previous_vote.choose_rating == str(0):
                self.vote = self.data['choose_rating']
            else:
                self.vote = 0

        obj = Vote.objects.get(pk=previous_vote.id)
        obj.choose_rating = self.vote
        obj.save()
        self.count_vote()

    def validate_user(self):
        values = self.content_object.voting.values_list('user', flat=True)
        if self.user.id in values:
            raise serializers.ValidationError('You have already voted')
        else:
            Vote.objects.create(
                user=self.user,
                content_type=self.data['content_type'],
                object_id=self.data['object_id'],
                choose_rating=self.data['choose_rating']
            )

    def count_vote(self):
        positive_rating = self.content_object.voting.filter(choose_rating=1).count()
        negative_rating = self.content_object.voting.filter(choose_rating=-1).count()
        self.content_object.vote_count = (positive_rating + (negative_rating * -1))
        self.content_object.save()
        return self.content_object

    def run_system(self):
        self.validate_user()


class CreateRecord:
    def __init__(self, user, data):
        self.user = user
        self.data = data

    def one_time_add(self):
        self.user.rating += 10
        self.user.save()
        return self.user

    def validate_time_create(self):
        get_user_record_by_date = Question.objects.filter(user=self.user,
                                                          created_at__date=datetime.date.today()).count() + 1
        number = {'NEW': 2,
                  'MIDL': 4,
                  'PRO': 6}

        if self.user.rank:
            if get_user_record_by_date <= number[self.user.rank]:
                if self.data.is_valid():
                    self.data.save(user=self.user)
                    self.one_time_add()
                return Response(self.data.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise serializers.ValidationError(f'You can create only {number[self.user.rank]} record(s) for one day')


class UserRating:

    def __init__(self, user):
        self.user = user
        self.mult_by = 10
        self.local_rating = 0

    def count_user_rating(self):
        question = Question.objects.filter(user=self.user.id)
        answer = Answer.objects.filter(user=self.user.id)
        comment = Comment.objects.filter(user=self.user.id)
        print(question.values_list('vote_count', flat=True))
        a = question.values_list('vote_count', flat=True),

        self.local_rating = self.mult_by * (question.count() + answer.count() + comment.count())
        self.user.rating = self.local_rating + 50

        if self.user.rating <= 100:
            self.user.rank = 'NEW'
        elif 100 < self.user.rating <= 300:
            self.user.rank = 'MIDL'
        elif 300 < self.user.rating <= 500:
            self.user.rank = 'PRO'
        elif self.user.rating > 500:
            self.user.is_staff = True
        self.user.save()
        return self.user



