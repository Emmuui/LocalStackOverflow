import os
import django
import unittest
from datetime import datetime, timedelta
from unittest import mock
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.contenttypes.models import ContentType
from .services import CountSystem


class CountSystemTest(unittest.TestCase):

    def setUp(self):
        self.mock_user = mock.Mock(user='admin', rating=100, rank='NEW', return_value='admin')
        self.current_date = datetime.now()
        self.mock_obj_id = mock.Mock(obj_id=1)
        self.ct = ContentType.objects.get(model='question')
        self.mock_content_type = mock.Mock(content_type=self.ct)

    def test_raise_exception_compare_vote(self):
        previous_vote = mock.Mock(user=self.mock_user, choose_rating='1',
                                  date_created_at=datetime.now())
        content_object = mock.Mock(id=self.mock_obj_id, user=self.mock_user,
                                   title='Hello', description='Description',
                                   created_at=datetime.now() - timedelta(days=10), vote_count=0)
        instance = CountSystem(user=self.mock_user, content_object=content_object,
                               content_type=self.mock_content_type, obj_id=self.mock_obj_id,
                               choose_rating=1, first_vote=None,
                               previous_vote=previous_vote, class_name=None)

        with self.assertRaises(Exception) as context:
            instance.compare_vote()
        self.assertEqual('You have already voted', str(context.exception))

    def test_if_previous_vote_equal_zero_and_rating_equal_one(self):
        previous_vote = mock.Mock(user=self.mock_user, choose_rating='0',
                                  date_created_at=datetime.now())
        mock_content_type = mock.Mock(content_type=self.ct)
        content_object = mock.Mock(id=self.mock_obj_id, user=self.mock_user,
                                   title='Hello', description='Description',
                                   created_at=datetime.now() - timedelta(days=10), vote_count=0)
        instance = CountSystem(user=self.mock_user, content_object=content_object,
                               content_type=mock_content_type, obj_id=self.mock_obj_id,
                               choose_rating=1, first_vote=None,
                               previous_vote=previous_vote, class_name=None)
        self.assertEqual(1, instance.compare_vote())

    def test_if_previous_vote_equal_zero_and_rating_equal_two(self):
        previous_vote = mock.Mock(user=self.mock_user, choose_rating='0',
                                  date_created_at=datetime.now())
        instance = CountSystem(user=self.mock_user, content_object=None,
                               content_type=None, obj_id=None,
                               choose_rating=-1, first_vote=None,
                               previous_vote=previous_vote, class_name=None)
        self.assertEqual(-1, instance.compare_vote())

    def test_if_previous_vote_equal_one_and_choose_rating_not_equal_previous(self):
        previous_vote = mock.Mock(user=self.mock_user, choose_rating='1',
                                  date_created_at=datetime.now())
        instance = CountSystem(user=self.mock_user, content_object=None,
                               content_type=None, obj_id=None,
                               choose_rating=-1, first_vote=None,
                               previous_vote=previous_vote, class_name=None)
        self.assertEqual(0, instance.compare_vote())

    def test_if_previous_minus_one_choose_rating_one(self):
        previous_vote = mock.Mock(user=self.mock_user, choose_rating='-1',
                                  date_created_at=datetime.now())
        content_object = mock.Mock(id=self.mock_obj_id, user=self.mock_user,
                                   title='Hello', description='Description',
                                   created_at=datetime.now() - timedelta(days=10), vote_count=0)
        instance = CountSystem(user=self.mock_user, content_object=content_object,
                               content_type=self.mock_content_type, obj_id=self.mock_obj_id,
                               choose_rating=1, first_vote=None,
                               previous_vote=previous_vote, class_name='Question')
        self.assertEqual(0, instance.compare_vote())

    def test_validate_user_to_vote_with_exception(self):
        self.mock_user = mock.Mock(user='admin', rating=25, rank='NEW', return_value='admin')
        instance = CountSystem(user=self.mock_user, content_object=None,
                               content_type=None, obj_id=None,
                               choose_rating=1, first_vote=None,
                               previous_vote=None, class_name=None)
        with self.assertRaises(Exception) as context:
            instance.validate_user_to_vote(self.mock_user.rating)
        self.assertEqual('Must be rating bigger than 50', str(context.exception))

    def test_validate_user_to_vote_without_exception(self):
        instance = CountSystem(user=self.mock_user, content_object=None,
                               content_type=None, obj_id=None,
                               choose_rating=None, first_vote=None,
                               previous_vote=None, class_name=None)
        rating = instance.validate_user_to_vote(self.mock_user.rating)
        self.assertEqual(100, rating)

    def test_validate_question_access_to_vote_with_exception(self):
        previous_vote = mock.Mock(user=self.mock_user, choose_rating='-1',
                                  date_created_at=datetime.now())
        content_object = mock.Mock(id=self.mock_obj_id, user=self.mock_user,
                                   title='Hello', description='Description',
                                   created_at=datetime.now() - timedelta(days=10), vote_count=0)
        instance = CountSystem(user=self.mock_user, content_object=content_object,
                               content_type=self.mock_content_type, obj_id=self.mock_obj_id,
                               choose_rating=1, first_vote=None,
                               previous_vote=previous_vote, class_name='Question')
        with self.assertRaises(Exception) as context:
            instance.validate_question_access_to_vote(self.current_date + timedelta(days=29))
        self.assertEqual('You can vote within 28 days after the creation of the question', str(context.exception))

    def test_validate_question_access_to_vote(self):
        previous_vote = mock.Mock(user=self.mock_user, choose_rating='-1',
                                  date_created_at=datetime.now())
        content_object = mock.Mock(id=self.mock_obj_id, user=self.mock_user,
                                   title='Hello', description='Description',
                                   created_at=datetime.now() - timedelta(days=10), vote_count=0)
        instance = CountSystem(user=self.mock_user, content_object=content_object,
                               content_type=self.mock_content_type, obj_id=self.mock_obj_id,
                               choose_rating=1, first_vote=None,
                               previous_vote=previous_vote, class_name='Question')
        validate = instance.validate_question_access_to_vote(self.current_date)
        self.assertEqual('You can vote question', validate)

    def test_validate_question_access_to_vote_if_not_question(self):
        previous_vote = mock.Mock(user=self.mock_user, choose_rating='-1',
                                  date_created_at=datetime.now())
        ct = ContentType.objects.get(model='comment')
        mock_content_type = mock.Mock(content_type=ct)
        content_object = mock.Mock(id=self.mock_obj_id, user=self.mock_user,
                                   title='Hello', description='Description',
                                   created_at=datetime.now() - timedelta(days=10), vote_count=0)
        instance = CountSystem(user=self.mock_user, content_object=content_object,
                               content_type=mock_content_type, obj_id=self.mock_obj_id,
                               choose_rating=1, first_vote=None,
                               previous_vote=previous_vote, class_name='Comment')
        validate = instance.validate_question_access_to_vote(self.current_date)
        self.assertEqual('You can vote comment or answer', validate)

    def test_validate_time_update_vote_with_exception(self):
        first_vote = mock.Mock(user=self.mock_user, choose_rating='-1',
                               date_created_at=datetime.now())
        content_object = mock.Mock(id=self.mock_obj_id, user=self.mock_user,
                                   title='Hello', description='Description',
                                   created_at=datetime.now() - timedelta(days=10), vote_count=0)
        instance = CountSystem(user=self.mock_user, content_object=content_object,
                               content_type=None, obj_id=self.mock_obj_id,
                               choose_rating=None, first_vote=first_vote,
                               previous_vote=None, class_name='Question')

        with self.assertRaises(Exception) as context:
            instance.validate_time_update_vote(self.current_date + timedelta(hours=4))
        self.assertEqual('You can update your vote only during 3 hours after creation', str(context.exception))

    def test_validate_time_update_vote_without_exception(self):
        content_object = mock.Mock(id=self.mock_obj_id, user=self.mock_user,
                                   title='Hello', description='Description',
                                   created_at=datetime.now() - timedelta(days=10), vote_count=0)
        instance = CountSystem(user=self.mock_user, content_object=content_object,
                               content_type=None, obj_id=None,
                               choose_rating=None, first_vote=None,
                               previous_vote=None, class_name='Comment')
        instance.validate_question_access_to_vote(self.current_date)
        self.assertEqual('You can update vote', 'You can update vote')

    @mock.patch.object(CountSystem, 'update_rating')
    @mock.patch.object(CountSystem, 'create_vote')
    def test_run_system_if_previous_vote_doesnt_exist(self, mock_create_vote, mock_update_rating):
        content_object = mock.Mock(id=self.mock_obj_id, user=self.mock_user,
                                   title='Hello', description='Description',
                                   created_at=datetime.now() - timedelta(days=10), vote_count=0)
        first_vote = mock.Mock(user=self.mock_user, choose_rating='1',
                               date_created_at=datetime.now())
        instance = CountSystem(user=self.mock_user, content_object=content_object,
                               content_type=self.mock_content_type, obj_id=self.mock_obj_id,
                               choose_rating=1, first_vote=first_vote,
                               previous_vote=None, class_name='Question')
        vote_mock = mock.Mock(user=self.mock_user, content_type=self.mock_content_type,
                              object_id=self.mock_obj_id, choose_rating=1,
                              return_value=self.mock_user)
        mock_create_vote.return_value = vote_mock.choose_rating
        mock_update_rating.return_value = 'update rating'
        run_system = instance.run_system(datetime.now())
        self.assertEqual(1, run_system)

    @mock.patch.object(CountSystem, 'update_rating')
    @mock.patch.object(CountSystem, 'create_vote')
    def test_run_system(self, mock_create_vote,  mock_update_rating):
        previous_vote = mock.Mock(user=self.mock_user, choose_rating='-1',
                                  date_created_at=datetime.now())
        content_object = mock.Mock(id=self.mock_obj_id, user=self.mock_user,
                                   title='Hello', description='Description',
                                   created_at=datetime.now() - timedelta(days=10), vote_count=0)
        first_vote = mock.Mock(user=self.mock_user, choose_rating='1',
                               date_created_at=datetime.now())
        instance = CountSystem(user=self.mock_user, content_object=content_object,
                               content_type=self.mock_content_type, obj_id=self.mock_obj_id,
                               choose_rating=1, first_vote=first_vote,
                               previous_vote=previous_vote, class_name='Question')
        vote_mock = mock.Mock(user=self.mock_user, content_type=self.mock_content_type,
                              object_id=self.mock_obj_id, choose_rating=0,
                              return_value=self.mock_user)
        mock_create_vote.return_value = vote_mock.choose_rating
        mock_update_rating.return_value = 'update rating'
        run_system = instance.run_system(datetime.now())
        self.assertEqual(run_system, vote_mock.choose_rating)
