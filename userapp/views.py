from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from .serializers import (UserListSerializer, RegisterSerializer, ImageUploadSerializer)
from .models import UserProfile
from .permissions import IsOwnerOnly
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


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
    # parser_classes = (MultiPartParser,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'description': openapi.Schema(type=openapi.TYPE_STRING, description='description'),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),
                    'second_name': openapi.Schema(type=openapi.TYPE_STRING, description='second_name')}
    ))
    def put(self, request):
        user = get_object_or_404(UserProfile.objects.all(), pk=self.request.user.id)
        serializer = UserListSerializer(user, data=request.data)
        self.check_object_permissions(request, user)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """ All user can get detail view of current user by pk """
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, pk, format=None):
        user = UserProfile.objects.filter(id=pk)
        serializer = UserListSerializer(user, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class OwnUserDataDetailView(APIView):
    """ All user can get detail view of current user by pk """
    permission_classes = (IsOwnerOnly, IsAdminUser)

    def get(self, request, format=None):
        user = UserProfile.objects.filter(id=self.request.user.id)
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


class ImageUploadView(APIView):
    permission_classes = (IsOwnerOnly, )
    parser_classes = (MultiPartParser, )

    @swagger_auto_schema(
        operation_description='Upload avatar',
        operation_id='Upload avatar file',
        manual_parameters=[openapi.Parameter(
            name="file",
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
            description="Document"
        )],
        responses={400: 'Invalid data in uploaded file',
                   200: 'Success'},
    )
    def put(self, request):
        queryset = UserProfile.objects.get(pk=self.request.user.id)
        serializer = ImageUploadSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
