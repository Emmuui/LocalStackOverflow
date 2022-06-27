import unittest
from unittest import mock
from .services import UserRating


class UserRatingTest(unittest.TestCase):
    def setUp(self):
        self.mock_user = mock.Mock(user='admin', rating=100, rank='NEW', is_staff=False, return_value='admin')
        self.instance = UserRating(self.mock_user)
        self.mult_by_mapping = {
            'NEW': 5,
            'MIDL': 10,
            'PRO': 15,
            'STAFF': 20
        }
        self.one_time_add = 5
        self.mult_by = self.mult_by_mapping[self.mock_user.rank]
        self.plus_vote = 1
        self.minus_vote = 1

    def test_rating_for_creation(self):
        self.assertEqual((self.mock_user.rating + self.one_time_add), self.instance.rating_for_creation_record())

    def test_plus_rating(self):
        rating = self.mock_user.rating + self.mult_by * self.plus_vote
        self.assertEqual(rating, self.instance.count_user_rating(self.plus_vote))

    def test_minus_rating(self):
        rating = self.mock_user.rating + self.mult_by * self.minus_vote
        self.assertEqual(rating, self.instance.count_user_rating(self.minus_vote))

    def test_add_new_rank_to_user(self):
        self.assertEqual(self.mock_user.rank, self.instance.add_rank_to_user())

    def test_add_midl_rank_to_user(self):
        self.mock_user.rating = 200
        self.mock_user.rank = 'MIDL'
        self.assertEqual(self.mock_user.rank, self.instance.add_rank_to_user())

    def test_add_pro_rank_to_user(self):
        self.mock_user.rating = 400
        self.mock_user.rank = 'PRO'
        self.assertEqual(self.mock_user.rank, self.instance.add_rank_to_user())

    def test_add_staff_rank_to_user(self):
        self.mock_user.rating = 501
        self.mock_user.rank = 'STAFF'
        self.assertEqual(self.mock_user.rank, self.instance.add_rank_to_user())
