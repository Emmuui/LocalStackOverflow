from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, serializers
from question.models import Question, Answer, Comment
import datetime


class CreateRecord:
    def __init__(self, user, data, model):
        self.user = user
        self.data = data
        self.model = model
        self.record_by_date = None
        self.instance = None

    def find_model(self):
        mapping = {
            'question': QuestionCreateService,
            'answer': AnswerCreateService,
            'comment': CommentCreateService
        }

        model = {
            'question': Question,
            'answer': Answer,
            'comment': Comment
        }
        self.record_by_date = model[self.model]
        self.instance = mapping[self.model]
        return self.validate_creation_record_per_day()

    def validate_creation_record_per_day(self):
        instance = self.instance(self.user, self.data, self.model)
        get_user_record_by_date = self.record_by_date.objects.filter(user=self.user,
                                                                     created_at__date=datetime.date.today()).count() + 1
        number = {'NEW': 2,
                  'MIDL': 4,
                  'PRO': 6}

        if self.user.rank:
            if get_user_record_by_date <= number[self.user.rank]:
                return instance.create_method()
            else:
                raise serializers.ValidationError(f'You can create only {number[self.user.rank]} record(s) for one day')


class QuestionCreateService(CreateRecord):
    def __init__(self, user, data, model):
        self.obj = None
        CreateRecord.__init__(self, user, data, model)

    def create_method(self):
        try:
            description = self.data['description']
        except KeyError:
            description = None

        self.obj = Question.objects.create(
            user=self.user,
            title=self.data['title'],
            description=description,
        )

        try:
            tags = self.data['tag']
            for tag in tags:
                self.obj.tag.add(tag)
            return self.obj
        except KeyError:
            pass

        return self.obj


class AnswerCreateService(CreateRecord):
    def __init__(self, user, data, model):
        self.obj = None
        CreateRecord.__init__(self, user, data, model)

    def create_method(self):
        try:
            description = self.data['description']
        except KeyError:
            description = None

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
        try:
            parent = self.data['parent']
        except KeyError:
            parent = None

        self.obj = Comment.objects.create(
            user=self.user,
            text=self.data['text'],
            parent=parent,
            content_type=self.data['content_type'],
            object_id=self.data['object_id']
        )

        return self.obj
