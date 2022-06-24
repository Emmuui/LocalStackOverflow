from vote.models import Vote
from userapp.services import UserRating
from datetime import datetime, timedelta
from .exceptions import TimeValidateException, BaseValidateException, RatingException
from userapp.models import UserProfile


class CountSystem:

    def __init__(self, user, data):
        self.data = data
        self.content_object = self.data.get('content_object')
        self.user = user
        user = UserProfile.objects.get(pk=1)
        print(user)
        print(self.data)
        self.obj = None
        self.rating_value = 0
        self.vote = 0
        self.user_rating = UserRating(user=self.user)
        self.previous_vote = self.content_object.voting.filter(user=self.user).last()

    def validate_time_update_vote(self):
        vote_instance = self.content_object.voting.filter(user=self.user).last()
        if self.content_object.__class__.__name__ == 'Question':
            time = vote_instance.date_created_at
            current_hours = datetime.now()
            if current_hours >= time + timedelta(hours=3):
                message = 'You can update your vote only during 3 hours after creation'
                raise TimeValidateException(message)

    def compare_vote(self):
        if self.previous_vote.choose_rating == self.data.get('choose_rating'):
            message = 'You have already voted'
            raise BaseValidateException(message)
        elif self.previous_vote.choose_rating == str(0):
            self.rating_value = self.data.get('choose_rating')
        elif self.previous_vote.choose_rating != self.data.get('choose_rating'):
            if self.previous_vote.choose_rating == str(-1):
                self.data['choose_rating'] = 0
                self.rating_value += 1
            elif self.previous_vote.choose_rating == str(1):
                self.data['choose_rating'] = 0
                self.rating_value -= 1

    def validate_question_access_to_vote(self):
        if self.content_object.__class__.__name__ == 'Question':
            date_created = self.content_object.created_at.date()
            current_date = datetime.now().date()
            if current_date >= date_created + timedelta(days=28):
                message = 'You can vote within 28 days after the creation of the question'
                raise TimeValidateException(message)

    def create_vote(self):
        self.obj = Vote.objects.create(
            user=self.user,
            content_type=self.data.get('content_type'),
            object_id=self.data.get('object_id'),
            choose_rating=self.data.get('choose_rating')
        )
        self.obj.save()
        return self.obj

    def update_vote_count(self):
        self.content_object.vote_count += int(self.data.get('choose_rating'))
        self.content_object.save()
        return self.content_object

    def update_rating(self):
        self.user_rating.count_user_rating(self.rating_value)
        return self.user_rating

    def validate_user_to_vote(self):
        if self.user.rating < 50:
            raise RatingException('Must be rating bigger than 50')

    def run_system(self):
        self.validate_user_to_vote()
        self.validate_question_access_to_vote()
        if self.previous_vote:
            self.validate_time_update_vote()
            self.compare_vote()
        else:
            self.rating_value = self.data.get('choose_rating')
        self.create_vote()
        self.update_vote_count()
        return self.update_rating()
