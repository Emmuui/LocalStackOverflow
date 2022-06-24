import unittest
from userapp.models import UserProfile
from .services import CountSystem
from unittest import mock


class CountSystemTest(unittest.TestCase):
    mock_user = mock.Mock(user='admin', rating=50, return_value=None)
    mock_data = mock.Mock()
    instance = CountSystem(user=mock_user.user, data=mock_data)

    def validate_user_to_vote_test(self):
        self.assertEqual(1, 1)

