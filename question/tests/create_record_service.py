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
        mock_model = 'Question'
        number = {'NEW': 2,
                  'MIDL': 4,
                  'PRO': 6}
        value = number[self.mock_user.rank]
        record_by_date = 3
        instance = CreateRecord(self.mock_user, mock_question_data, mock_model, record_by_date)
        with self.assertRaises(Exception) as context:
            instance.validate_creation_record_per_day()
        self.assertEqual(f'You can create only {value} record(s) for one day', str(context.exception))

    def test_validate_creation_record_per_day_without_exception(self):
        mock_question_data = mock.Mock(title='title', tag=[1, 2], description='Hello')
        mock_model = 'Comment'
        record_by_date = 1
        instance = CreateRecord(self.mock_user, mock_question_data, mock_model, record_by_date)
        self.assertEqual('You can create record', instance.validate_creation_record_per_day())

    @mock.patch.object(QuestionCreateService, 'create_method')
    def test_run_system_if_model_is_question(self, create_method):
        mock_model = 'Question'
        mock_question_data = mock.Mock(title='Hello', tag=[1, 2], description='Hello')
        record_by_date = 1
        create_method.return_value = mock_question_data.title

        instance = CreateRecord(self.mock_user, mock_question_data, mock_model, record_by_date)
        self.assertEqual('Hello', instance.run_system())

    @mock.patch.object(AnswerCreateService, 'create_method')
    def test_run_system_if_model_is_answer(self, create_method):
        mock_model = 'Answer'
        mock_question_data = mock.Mock(title='How are you?', question=1)
        record_by_date = 1
        create_method.return_value = f'{mock_question_data.title} - {mock_question_data.question}'
        instance = CreateRecord(self.mock_user, mock_question_data, mock_model, record_by_date)
        self.assertEqual(f'{mock_question_data.title} - {mock_question_data.question}', instance.run_system())

    @mock.patch.object(CommentCreateService, 'create_method')
    def test_run_system_if_model_is_comment(self, create_method):
        mock_model = 'Comment'
        mock_question_data = mock.Mock(text='How are you?', content_type='question', object_id=1)
        record_by_date = 1
        create_method.return_value = mock_question_data.content_type
        instance = CreateRecord(self.mock_user, mock_question_data, mock_model, record_by_date)
        self.assertEqual('question', instance.run_system())
