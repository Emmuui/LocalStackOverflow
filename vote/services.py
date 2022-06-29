from vote.models import Vote
from userapp.services import UserRating
from datetime import timedelta
from .exceptions import TimeValidateException, BaseValidateException, RatingException


class CountSystem:

    def __init__(self, user, content_object, content_type, obj_id,
                 choose_rating, first_vote, previous_vote, class_name):
        self.user = user
        self.content_object = content_object
        self.content_type = content_type
        self.obj_id = obj_id
        self.choose_rating = choose_rating
        self.first_vote = first_vote
        self.previous_vote = previous_vote
        self.class_name = class_name
        self.value = 0
        self.user_rating = None
        self.obj = None

    def validate_time_update_vote(self, current_hours):
        if self.class_name == 'Question':
            time = self.first_vote.date_created_at
            if current_hours >= time + timedelta(hours=3):
                message = 'You can update your vote only during 3 hours after creation'
                raise TimeValidateException(message)
        return 'You can update vote'

    def compare_vote(self) -> int:
        if self.previous_vote.choose_rating == str(self.choose_rating):
            message = 'You have already voted'
            raise BaseValidateException(message)
        elif self.previous_vote.choose_rating == str(0):
            self.value = self.choose_rating
        elif self.previous_vote.choose_rating != self.choose_rating:
            if self.previous_vote.choose_rating == str(-1):
                self.choose_rating = 0
                self.value += 1
            elif self.previous_vote.choose_rating == str(1):
                self.choose_rating = 0
                self.value -= 1
        return self.choose_rating

    def validate_question_access_to_vote(self, current_date) -> str:
        if self.class_name == 'Question':
            date_created = self.content_object.created_at
            if current_date >= date_created + timedelta(days=28):
                message = 'You can vote within 28 days after the creation of the question'
                raise TimeValidateException(message)
            return 'You can vote question'
        else:
            return 'You can vote comment or answer'

    def create_vote(self):
        self.obj = Vote.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.obj_id,
            choose_rating=self.choose_rating
        )
        self.obj.save()
        return self.obj

    def update_vote_count(self):
        self.content_object.vote_count += int(self.value)
        self.content_object.save()
        return self.content_object.vote_count

    def update_rating(self):
        self.user_rating = UserRating(user=self.user)
        self.user_rating.run_system(self.value)
        return self.user_rating

    def validate_user_to_vote(self, rating: int) -> int:
        if rating < 50:
            raise RatingException('Must be rating bigger than 50')
        return rating

    def run_system(self, datetime_now):
        self.validate_user_to_vote(self.user.rating)
        self.validate_question_access_to_vote(datetime_now)
        if self.previous_vote:
            self.validate_time_update_vote(datetime_now)
            self.compare_vote()
        else:
            self.value = self.choose_rating
        self.update_vote_count()
        self.update_rating()
        return self.create_vote()

