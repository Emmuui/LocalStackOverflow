from vote.models import Vote
from rest_framework import serializers
from userapp.services import UserRating
from datetime import datetime, timedelta


class CountSystem:

    def __init__(self, user, data):
        self.content_object = data['content_object']
        self.data = data
        self.user = user
        self.update_obj = None
        self.obj = None
        self.number = 0
        self.vote = 0
        self.user_rating = UserRating(user=self.user)
        self.users_vote_list = self.content_object.voting.values_list('user', flat=True)

    def validate_time_update_vote(self):
        vote_instance = self.content_object.voting.get(user=self.user)
        time = vote_instance.date_created_at
        current_hours = datetime.now()
        if current_hours <= time+timedelta(hours=3):
            self.update_vote()
        else:
            raise serializers.ValidationError('You can update your vote only during 3 hours after creation')

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
            self.vote = 0
            self.number = 0
        self.update_obj = Vote.objects.get(pk=previous_vote.id)
        self.update_obj.choose_rating = self.vote
        self.update_obj.save()
        self.calculate_vote()

    def create_or_update_vote(self):
        if self.user.id in self.users_vote_list:
            return self.validate_time_update_vote()
        else:
            return self.create_vote()

    def validate_question_access_to_vote(self):
        if self.content_object.__class__.__name__ == 'Question':
            date_created = self.content_object.created_at.date()
            current_date = datetime.now().date()
            if current_date <= date_created + timedelta(days=28):
                self.create_or_update_vote()
            else:
                raise serializers.ValidationError('You can vote within 28 days after the creation of the question')
        else:
            self.create_or_update_vote()

    def create_vote(self):
        self.obj = Vote.objects.create(
            user=self.user,
            content_type=self.data['content_type'],
            object_id=self.data['object_id'],
            choose_rating=self.data['choose_rating']
        )
        self.calculate_vote()

    def calculate_vote(self):
        if self.obj:
            self.user_rating.rating_for_vote(number=self.obj.choose_rating)
            self.content_object.vote_count += int(self.obj.choose_rating)
        elif self.update_obj:
            self.user_rating.rating_for_vote(number=self.number)
            self.content_object.vote_count += int(self.number)
        self.content_object.save()
        return self.content_object

    def run_system(self):
        return self.validate_question_access_to_vote()
