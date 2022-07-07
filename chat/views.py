from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MessageToUser, Chat
from .serializers import MessageToUserSerializer, ListOfChatToOneUserSerializer,\
    MessageListByOneChatSerializer
from .services import MessageService
from django.shortcuts import render


def render_test_page(request, group_name):
    return render(request, 'chat/test.html', {'groupname': group_name})


class MessageToUserCreateView(APIView):

    def post(self, request):
        serializer = MessageToUserSerializer(data=self.request.data)
        if serializer.is_valid():
            service = MessageService(data=serializer.validated_data)
            obj = service.run_system()
            output_serializer = MessageListByOneChatSerializer(obj, many=True)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetListChatUser(APIView):

    def get(self, request):
        queryset = Chat.objects.filter(members=self.request.user.id)
        serializer = ListOfChatToOneUserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllMessageFromOneChat(APIView):
    # permission_classes = (IsOwnerOnly, )

    def get(self, request, pk):
        queryset = MessageToUser.objects.filter(chat=pk)
        serializer = MessageListByOneChatSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
