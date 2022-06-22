from django.test import TestCase
from vote.models import Vote
from userapp.models import UserProfile
from .services import CountSystem


class CountSystemTest(TestCase):
    user = UserProfile.objects.create(user='test', rating=100, rank='NEW')

    def validate_user_to_vote_test(self):
        pass

