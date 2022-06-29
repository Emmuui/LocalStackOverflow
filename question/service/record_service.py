import datetime
from question.models import Question, Answer, Comment
from question.exceptions import RecordPerDayException


class CreateRecord:
    def __init__(self, user, data, model):
        self.user = user
        self.data = data
        self.model = model
        self.record_by_date = None
        self.instance = None
        mapping = {
            'question': QuestionCreateService,
            'answer': AnswerCreateService,
            'comment': CommentCreateService
        }
        model_mapping = {
            'question': Question,
            'answer': Answer,
            'comment': Comment
        }
        self.model_instance = model_mapping[self.model]
        self.instance = mapping[self.model]

    def validate_creation_record_per_day(self, record_by_date):
        number = {'NEW': 2,
                  'MIDL': 4,
                  'PRO': 6}
        value = number[self.user.rank]
        if record_by_date >= value:
            raise RecordPerDayException(f'You can create only {value} record(s) for one day')
        return 'You can create record'

    def run_system(self):
        self.record_by_date = self.model_instance.objects.filter(user=self.user,
                                                                 created_at__date=datetime.date.today()).count()
        self.validate_creation_record_per_day(self.record_by_date)
        self.instance = self.instance(self.user, self.data, self.model)
        return self.instance.create_method()


class QuestionCreateService(CreateRecord):
    def __init__(self, user, data, model):
        self.obj = None
        CreateRecord.__init__(self, user, data, model)

    def create_method(self):
        description = self.data.get('description', None)
        self.obj = Question.objects.create(
            user=self.user,
            title=self.data['title'],
            description=description,
        )

        tags = self.data.get('tag', [])
        for tag in tags:
            self.obj.tag.add(tag)
        return self.obj


class AnswerCreateService(CreateRecord):
    def __init__(self, user, data, model):
        self.obj = None
        CreateRecord.__init__(self, user, data, model)

    def create_method(self):
        description = self.data.get('description', None)

        self.obj = Answer.objects.create(
            user=self.user,
            title=self.data['title'],
            description=description,
            question=self.data['question']
        )

        return self.obj


class CommentCreateService(CreateRecord):
    def __init__(self, user, data, model):
        self.obj = None
        CreateRecord.__init__(self, user, data, model)

    def create_method(self):
        parent = self.data.get('parent', None)

        self.obj = Comment.objects.create(
            user=self.user,
            text=self.data['text'],
            parent=parent,
            content_type=self.data['content_type'],
            object_id=self.data['object_id']
        )

        return self.obj

