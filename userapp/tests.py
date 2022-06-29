import unittest
from unittest import mock
from .services import UserRating


class UserRatingTest(unittest.TestCase):
    def setUp(self):
        self.mult_by_mapping = {
            'NEW': 5,
            'MIDL': 10,
            'PRO': 15,
            'STAFF': 20
        }
        self.one_time_add = 5
        self.plus_vote = 1
        self.minus_vote = -1

    def test_rating_for_creation(self):
        mock_user = mock.Mock(user='admin', rating=100, rank='NEW', is_staff=False, return_value='admin')
        instance = UserRating(mock_user)
        self.assertEqual((mock_user.rating + self.one_time_add), instance.rating_for_creation_record())

    def test_plus_rating(self):
        mock_user = mock.Mock(user='admin', rating=100, rank='NEW', is_staff=False, return_value='admin')
        instance = UserRating(mock_user)
        mult_by = self.mult_by_mapping[mock_user.rank]
        rating = mock_user.rating + mult_by * self.plus_vote
        self.assertEqual(rating, instance.count_user_rating(self.plus_vote))

    def test_minus_rating(self):
        mock_user = mock.Mock(user='admin', rating=100, rank='NEW', is_staff=False, return_value='admin')
        instance = UserRating(mock_user)
        mult_by = self.mult_by_mapping[mock_user.rank]
        rating = mock_user.rating + mult_by * self.minus_vote
        self.assertEqual(rating, instance.count_user_rating(self.minus_vote))

    def test_add_new_rank_to_user(self):
        mock_user = mock.Mock(user='admin', rating=100, rank='NEW', is_staff=False, return_value='admin')
        instance = UserRating(mock_user)
        self.assertEqual(mock_user.rank, instance.add_rank_to_user())

    def test_add_midl_rank_to_user(self):
        mock_user = mock.Mock(user='admin', rating=105, rank='NEW', is_staff=False, return_value='admin')
        instance = UserRating(mock_user)
        new_rank = mock_user.rank = 'MIDL'
        self.assertEqual(new_rank, instance.add_rank_to_user())

    def test_add_pro_rank_to_user(self):
        mock_user = mock.Mock(user='admin', rating=305, rank='MIDL', is_staff=False, return_value='admin')
        instance = UserRating(mock_user)
        new_rank = mock_user.rank = 'PRO'
        self.assertEqual(new_rank, instance.add_rank_to_user())

    def test_add_staff_rank_to_user(self):
        mock_user = mock.Mock(user='admin', rating=505, rank='MIDL', is_staff=False, return_value='admin')
        instance = UserRating(mock_user)
        new_rank = mock_user.rank = 'STAFF'
        self.assertEqual(new_rank, instance.add_rank_to_user())

    def test_run_system(self):
        mock_user = mock.Mock(user='admin', rating=105, rank='MIDL', is_staff=False, return_value='admin')
        instance = UserRating(mock_user)
        rank = 'NEW'
        self.assertEqual(rank, instance.run_system(self.minus_vote))
