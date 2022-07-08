import serializer as serializer
from asgiref.sync import async_to_sync, sync_to_async
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MessageToUser, Chat
from .serializers import MessageToUserSerializer, ListOfChatToOneUserSerializer,\
    MessageListByOneChatSerializer, OutPutUserMessageSerializer
from .services import MessageService
from channels.layers import get_channel_layer


class MessageToUserCreateView(APIView):

    def post(self, request):
        serializer = MessageToUserSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        service = MessageService(author=request.user.id,
                                 text=serializer.validated_data.get('text'),
                                 recipient=serializer.validated_data.get('recipient'),
                                 chat=serializer.validated_data.get('chat'))
        obj = service.run_system()
        test_group_name = str(obj.author.id)
        print(test_group_name)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            test_group_name,
            {
                'type': 'chat_message',
                'author': obj.author.username,
                'message': obj.text,
                'created_at': obj.created_at
            }
        )
        output_serializer = OutPutUserMessageSerializer(obj)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


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
