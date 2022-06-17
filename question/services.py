from rest_framework.response import Response
from rest_framework import status, serializers
from question.models import Question, Answer, Comment
import datetime


class CreateRecord:
    def __init__(self, user, data):
        self.user = user
        self.data = data

    def one_time_add(self):
        self.user.rating += 10
        self.user.save()
        return self.user

    def validate_time_create(self):
        get_user_record_by_date = Question.objects.filter(user=self.user,
                                                          created_at__date=datetime.date.today()).count() + 1
        number = {'NEW': 2,
                  'MIDL': 4,
                  'PRO': 6}

        print(self.data)
        if self.user.rank:
            if get_user_record_by_date <= number[self.user.rank]:
                if self.data.is_valid():
                    self.data.save(user=self.user)
                    self.one_time_add()
                return Response(self.data.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise serializers.ValidationError(f'You can create only {number[self.user.rank]} record(s) for one day')



