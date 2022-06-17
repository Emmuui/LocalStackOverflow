from rest_framework.response import Response
from rest_framework import status, serializers
from question.models import Question, Answer, Comment
from question.service.create_record import CreateInstance
import datetime


class CreateRecord:
    def __init__(self, user, data, model):
        self.user = user
        self.data = data
        self.model = model
        self.instance = None

    def one_time_add(self):
        self.user.rating += 10
        self.user.save()
        return self.user

    def find_model(self):
        model = {
            'question': Question,
            'answer': Answer,
            'comment': Comment
        }
        self.instance = model[self.model]
        self.validate_time_create()

    def validate_time_create(self):
        instance = CreateInstance(user=self.user, model=self.instance, data=self.data)
        get_user_record_by_date = self.instance.objects.filter(user=self.user,
                                                               created_at__date=datetime.date.today()).count() + 1
        number = {'NEW': 2,
                  'MIDL': 4,
                  'PRO': 6}

        print(self.data)
        if self.user.rank:
            if get_user_record_by_date <= number[self.user.rank]:
                instance.decide_to_create()
            else:
                raise serializers.ValidationError(f'You can create only {number[self.user.rank]} record(s) for one day')
