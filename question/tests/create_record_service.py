import os
import django
import unittest
from unittest import mock

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from question.service.record_service import CreateRecord, QuestionCreateService,\
    AnswerCreateService, CommentCreateService


class CountSystemTest(unittest.TestCase):
    def setUp(self):
        self.mock_user = mock.Mock(user='admin', rating=100, rank='NEW', return_value='admin')

    def test_validate_creation_record_per_day_with_exception(self):
        mock_question_data = mock.Mock(title='title', tag=[1, 2], description='Hello')
        mock_model = 'question'
        number = {'NEW': 2,
                  'MIDL': 4,
                  'PRO': 6}
        value = number[self.mock_user.rank]
        instance = CreateRecord(self.mock_user, mock_question_data, mock_model)
        with self.assertRaises(Exception) as context:
            instance.validate_creation_record_per_day(value)
        self.assertEqual(f'You can create only {value} record(s) for one day', str(context.exception))

    def test_validate_creation_record_per_day_without_exception(self):
        mock_question_data = mock.Mock(title='title', tag=[1, 2], description='Hello')
        mock_model = 'question'
        number = {'NEW': 2,
                  'MIDL': 4,
                  'PRO': 6}
        value = number[self.mock_user.rank]
        instance = CreateRecord(self.mock_user, mock_question_data, mock_model)
        self.assertEqual('You can create record', instance.validate_creation_record_per_day(value-1))


