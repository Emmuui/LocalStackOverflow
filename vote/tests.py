import unittest
import datetime
from unittest import mock
from django.contrib.contenttypes.models import ContentType
from .services import CountSystem
from .exceptions import RatingException


class CountSystemTest(unittest.TestCase):
    def setUp(self):
        self.mock_user = mock.Mock(user='admin', rating=100, rank='NEW', return_value='admin')
        self.mock_obj_id = mock.Mock(obj_id=1)
        self.content_object = mock.Mock(id=self.mock_obj_id, user=self.mock_user,
                                        title='Hello', description='Description',
                                        created_at=datetime.datetime(2022, 6, 27, 12, 0, 3, 851822), vote_count=0)
        ct = ContentType.objects.get(model='question')
        self.mock_content_type = mock.Mock(content_type=ct)
        self.choose_rating = 1
        self.instance = CountSystem(user=self.mock_user, content_object=self.content_object,
                                    content_type=self.mock_content_type, obj_id=self.mock_obj_id,
                                    choose_rating=self.choose_rating)

    def test_exception_compare_vote(self):
        with self.assertRaises(Exception) as context:
            vote = 1
            self.instance.compare_vote(vote)
        self.assertEqual('You have already voted', str(context.exception))

    def test_prev_vote_equal_zero_vote(self):
        vote = '0'
        if self.choose_rating == 1:
            self.assertEqual(1, self.instance.compare_vote(vote))
        elif self.choose_rating == -1:
            self.assertEqual(-1, self.instance.compare_vote(vote))

    def test_compare_vote(self):
        vote = '-1'
        if self.choose_rating == 1:
            self.assertEqual(0, self.instance.compare_vote(vote))
        elif self.choose_rating == -1:
            self.assertEqual(0, self.instance.compare_vote(vote))

    def test_validate_user_to_vote_with_exception(self):
        with self.assertRaises(Exception) as context:
            rating = 25
            self.instance.validate_user_to_vote(rating)
        self.assertEqual('Must be rating bigger than 50', str(context.exception))

    def test_validate_user_to_vote_without_exception(self):
        rating = self.instance.validate_user_to_vote(self.mock_user.rating)
        self.assertEqual(self.mock_user.rating, rating)

    def test_validate_question_access_to_vote(self):
        instance = self.instance.validate_question_access_to_vote('Question')
        self.assertEqual('You can vote question', instance)

    def test_validate_question_access_to_vote_if_not_question(self):
        instance = self.instance.validate_question_access_to_vote('Comment')
        self.assertEqual('You can vote comment or answer', instance)

    def test_update_vote_count_first(self):
        self.instance.choose_rating = -1
        instance = self.instance.update_vote_count()
        self.assertEqual(-1, instance)

    def test_update_vote_count_second(self):
        self.instance.choose_rating = 1
        instance = self.instance.update_vote_count()
        self.assertEqual(1, instance)
