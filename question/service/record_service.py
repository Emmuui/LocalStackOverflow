from question.models import Question, Answer, Comment
from question.exceptions import RecordPerDayException


class CreateRecord:
    def __init__(self, user, data, model, record_by_date):
        self.user = user
        self.data = data
        self.model = model
        self.record_by_date = record_by_date
        self.instance = None
        mapping = {
            'Question': QuestionCreateService,
            'Answer': AnswerCreateService,
            'Comment': CommentCreateService
        }
        self.instance = mapping[self.model]

    def validate_creation_record_per_day(self):
        number = {'NEW': 2,
                  'MIDL': 4,
                  'PRO': 6}
        value = number[self.user.rank]
        if self.record_by_date >= value:
            raise RecordPerDayException(f'You can create only {value} record(s) for one day')
        return 'You can create record'

    def run_system(self):
        self.validate_creation_record_per_day()
        self.instance = self.instance(self.user, self.data, self.model, self.record_by_date)
        return self.instance.create_method()


class QuestionCreateService(CreateRecord):
    def __init__(self, user, data, model, record_by_date):
        self.obj = None
        CreateRecord.__init__(self, user, data, model, record_by_date)

    def create_method(self):
        self.obj = Question.objects.create(
            user=self.user,
            title=self.data['title'],
            description=self.data.get('description', None),
        )

        tags = self.data.get('tag', [])
        for tag in tags:
            self.obj.tag.add(tag)
        return self.obj


class AnswerCreateService(CreateRecord):
    def __init__(self, user, data, model, record_by_date):
        self.obj = None
        CreateRecord.__init__(self, user, data, model, record_by_date)

    def create_method(self):

        self.obj = Answer.objects.create(
            user=self.user,
            title=self.data['title'],
            description=self.data.get('description', None),
            question=self.data['question']
        )

        return self.obj


class CommentCreateService(CreateRecord):
    def __init__(self, user, data, model, record_by_date):
        self.obj = None
        CreateRecord.__init__(self, user, data, model, record_by_date)

    def create_method(self):

        self.obj = Comment.objects.create(
            user=self.user,
            text=self.data.get('text'),
            parent=self.data.get('parent', None),
            content_type=self.data.get('content_type'),
            object_id=self.data.get('object_id')
        )

        return self.obj

