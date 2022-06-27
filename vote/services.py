from vote.models import Vote
from userapp.services import UserRating
from datetime import datetime, timedelta
from .exceptions import TimeValidateException, BaseValidateException, RatingException


class CountSystem:

    def __init__(self, user, content_object, content_type, obj_id, choose_rating):
        self.user = user
        self.content_object = content_object
        self.content_type = content_type
        self.obj_id = obj_id
        self.choose_rating = choose_rating
        self.rating_value = 0
        self.vote = 0
        self.user_rating = None
        self.previous_vote = None

    def validate_time_update_vote(self):
        vote_instance = self.content_object.voting.filter(user=self.user).last()
        question = self.content_object.__class__.__name__
        if question == 'Question':
            time = vote_instance.date_created_at
            current_hours = datetime.now()
            if current_hours >= time + timedelta(hours=3):
                message = 'You can update your vote only during 3 hours after creation'
                raise TimeValidateException(message)

    def compare_vote(self, previous_vote):
        if previous_vote == self.choose_rating:
            message = 'You have already voted'
            raise BaseValidateException(message)
        elif previous_vote == str(0):
            self.rating_value = self.choose_rating
        elif previous_vote != self.choose_rating:
            if previous_vote == str(-1):
                self.choose_rating = 0
                self.rating_value += 1
            elif previous_vote == str(1):
                self.choose_rating = 0
                self.rating_value -= 1
        return self.choose_rating

    def validate_question_access_to_vote(self, question):
        if question == 'Question':
            date_created = self.content_object.created_at.date()
            current_date = datetime.now().date()
            if current_date >= date_created + timedelta(days=28):
                message = 'You can vote within 28 days after the creation of the question'
                raise TimeValidateException(message)
            return 'You can vote question'
        else:
            return 'You can vote comment or answer'

    def create_vote(self):
        obj = Vote.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.obj_id,
            choose_rating=self.choose_rating
        )
        obj.save()
        return obj

    def update_vote_count(self):
        self.content_object.vote_count += int(self.choose_rating)
        self.content_object.save()
        return self.content_object.vote_count

    def update_rating(self):
        self.user_rating = UserRating(user=self.user)
        self.user_rating.run_system(self.rating_value)
        return self.user_rating

    def validate_user_to_vote(self, rating):
        if rating < 50:
            raise RatingException('Must be rating bigger than 50')
        return rating

    def run_system(self):
        self.previous_vote = self.content_object.voting.filter(user=self.user).last()
        self.validate_user_to_vote(self.user.rating)
        self.validate_question_access_to_vote(self.content_object.__class__.__name__)
        if self.previous_vote:
            self.validate_time_update_vote()
            self.compare_vote(self.previous_vote.choose_rating)
        else:
            self.rating_value = self.choose_rating
        self.create_vote()
        self.update_vote_count()
        return self.update_rating()
