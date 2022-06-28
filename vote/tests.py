import unittest
from datetime import datetime, timedelta
from unittest import mock
from django.contrib.contenttypes.models import ContentType
from .services import CountSystem


class CountSystemTest(unittest.TestCase):
    def setUp(self):
        self.mock_user = mock.Mock(user='admin', rating=100, rank='NEW', return_value='admin')
        self.mock_obj_id = mock.Mock(obj_id=1)
        self.content_object = mock.Mock(id=self.mock_obj_id, user=self.mock_user,
                                        title='Hello', description='Description',
                                        created_at=datetime.now() - timedelta(days=10), vote_count=0)
        ct = ContentType.objects.get(model='question')
        self.mock_content_type = mock.Mock(content_type=ct)
        self.choose_rating = 1
        self.first_vote = mock.Mock(user=self.mock_user, choose_rating='1',
                                    date_created_at=datetime.now())
        self.previous_vote = mock.Mock(user=self.mock_user, choose_rating='1',
                                       date_created_at=datetime.now())
        self.instance = CountSystem(user=self.mock_user, content_object=self.content_object,
                                    content_type=self.mock_content_type, obj_id=self.mock_obj_id,
                                    choose_rating=self.choose_rating, first_vote=self.first_vote,
                                    previous_vote=self.previous_vote, class_name='Question')
        self.current_date = datetime.now()

    def test_exception_compare_vote(self):
        with self.assertRaises(Exception) as context:
            self.instance.compare_vote()
        self.assertEqual('You have already voted', str(context.exception))

    def test_prev_vote_equal_zero_vote(self):
        self.previous_vote.choose_rating = '0'
        if self.choose_rating == 1:
            self.assertEqual(1, self.instance.compare_vote())
        elif self.choose_rating == -1:
            self.assertEqual(-1, self.instance.compare_vote())

    def test_compare_vote(self):
        self.previous_vote.choose_rating = '-1'
        if self.instance.choose_rating == 1:
            self.assertEqual(0, self.instance.compare_vote())
        elif self.instance.choose_rating == -1:
            self.assertEqual(0, self.instance.compare_vote())

    def test_validate_user_to_vote_with_exception(self):
        with self.assertRaises(Exception) as context:
            rating = 25
            self.instance.validate_user_to_vote(rating)
        self.assertEqual('Must be rating bigger than 50', str(context.exception))

    def test_validate_user_to_vote_without_exception(self):
        rating = self.instance.validate_user_to_vote(self.mock_user.rating)
        self.assertEqual(self.mock_user.rating, rating)

    def test_validate_question_access_to_vote_with_exception(self):
        with self.assertRaises(Exception) as context:
            self.instance.validate_question_access_to_vote(self.current_date + timedelta(days=29))
        self.assertEqual('You can vote within 28 days after the creation of the question', str(context.exception))

    def test_validate_question_access_to_vote(self):
        instance = self.instance.validate_question_access_to_vote(self.current_date)
        self.assertEqual('You can vote question', instance)

    def test_validate_question_access_to_vote_if_not_question(self):
        self.instance.class_name = 'Comment'
        instance = self.instance.validate_question_access_to_vote(self.current_date)
        self.assertEqual('You can vote comment or answer', instance)

    def test_update_vote_count_first(self):
        self.instance.choose_rating = -1
        instance = self.instance.update_vote_count()
        self.assertEqual(-1, instance)

    def test_update_vote_count_second(self):
        self.instance.choose_rating = 1
        instance = self.instance.update_vote_count()
        self.assertEqual(1, instance)

    def test_validate_time_update_vote_exception(self):
        with self.assertRaises(Exception) as context:
            self.instance.validate_question_access_to_vote(self.current_date + timedelta(hours=3))
        self.assertEqual('You can update your vote only during 3 hours after creation', str(context.exception))

    def test_validate_time_update_vote_without_exception(self):
        self.instance.validate_question_access_to_vote(self.current_date)
        self.assertEqual('You can update vote', 'You can update vote')

