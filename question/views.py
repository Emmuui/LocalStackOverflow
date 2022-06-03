from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Question
from .serializers import QuestionSerializer, CreateQuestionSerializer


class QuestionListView(APIView):
    """ Get all question by id of user """

    def get(self, request, pk):
        print(self.request.user)
        queryset = Question.objects.filter(username__pk=self.request.user.id)
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    """ Create question view """

    def post(self, request):
        serializer = CreateQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
