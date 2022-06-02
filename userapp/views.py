from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .serializers import UserUpdateSerializer
from .models import *
from .permissions import IsOwnerOrReadOnly


class UserListView(generics.ListAPIView):
    """ ListView for all users """

    permission_classes = [IsAdminUser]
    queryset = UserProfile.objects.all()
    serializer_class = UserUpdateSerializer


class UserDetailView(APIView):

    def get(self, request, pk, format=None):
        user = UserProfile.objects.filter(id=pk)
        serializer = UserUpdateSerializer(user, many=True)
        if request.user == UserProfile.objects.get(id=pk):
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

