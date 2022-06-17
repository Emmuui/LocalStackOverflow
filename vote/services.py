from question.models import Question, Answer, Comment
from vote.models import Vote
from rest_framework import status, serializers


class CountSystem:

    def __init__(self, user, data):
        self.content_object = data['content_object']
        self.data = data
        self.user = user
        self.update_obj = None
        self.obj = None
        self.number = 0
        self.vote = 0

    def update_vote(self):
        next_vote = self.data['choose_rating']
        previous_vote = self.content_object.voting.get(user=self.user)
        if previous_vote.choose_rating != next_vote:
            if previous_vote.choose_rating == str(0):
                self.vote = self.data['choose_rating']
                self.number = self.data['choose_rating']
            else:
                self.vote = 0
                if previous_vote.choose_rating == str(-1):
                    self.number = 1
                elif previous_vote.choose_rating == str(1):
                    self.number = -1
        elif previous_vote.choose_rating == next_vote:
            self.vote = self.data['choose_rating']
            self.number = 0
        self.update_obj = Vote.objects.get(pk=previous_vote.id)
        self.update_obj.choose_rating = self.vote
        self.update_obj.save()
        self.calculate_vote()

    def validate_user(self):
        values = self.content_object.voting.values_list('user', flat=True)
        if self.user.id in values:
            raise serializers.ValidationError('You have already voted')
        else:
            self.obj = Vote.objects.create(
                user=self.user,
                content_type=self.data['content_type'],
                object_id=self.data['object_id'],
                choose_rating=self.data['choose_rating']
            )
            self.calculate_vote()

    def calculate_vote(self):
        if self.obj:
            self.content_object.vote_count += int(self.obj.choose_rating)
        elif self.update_obj:
            self.content_object.vote_count += int(self.number)
        self.content_object.save()

    def run_system(self):
        self.validate_user()


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



