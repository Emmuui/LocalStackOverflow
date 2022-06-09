from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from .serializers import (UserListSerializer, RegisterSerializer)
from .models import UserProfile
from .permissions import IsOwnerOnly


class RegisterView(APIView):
    """ Registration view for all user """
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PutUserDetailView(APIView):
    """ Only owner or is_staff user has access to this view """
    permission_classes = (IsAdminUser, IsOwnerOnly)

    def put(self, request, pk):
        user = get_object_or_404(UserProfile.objects.all(), pk=pk)
        serializer = UserListSerializer(user, data=request.data)
        self.check_object_permissions(request, user)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserDetailView(APIView):
    """ All user can get detail view of current user by pk """
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, pk, format=None):
        user = UserProfile.objects.filter(id=pk)
        serializer = UserListSerializer(user, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class GetUserListView(APIView):
    """ Only is_staff user can get list of all users """

    permission_classes = (IsAdminUser,)

    def get(self, request):

        user = UserProfile.objects.all()
        serializer = UserListSerializer(user, many=True)
        self.check_object_permissions(request, user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
