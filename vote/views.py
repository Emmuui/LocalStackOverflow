from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import *
from .models import Vote
from .serializers import *


class VoteCreateView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteListView(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request):
        queryset = Vote.objects.all()
        serializer = VoteSerializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class VoteUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        queryset = Vote.objects.filter(username__pk=self.request.user.id)
        serializer = VoteSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
