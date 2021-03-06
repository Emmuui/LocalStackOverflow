from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from userapp.models import UserProfile
from .models import MessageToUser, Chat


class MessageService:
    def __init__(self, author, text, recipient, chat):
        self.author = author
        self.text = text
        self.chat = chat
        self.recipient = recipient
        self.get_or_create_chat = None
        self.author_userprofile_instance = UserProfile.objects.get(pk=self.author)

    def get_chat(self):
        try:
            self.get_or_create_chat = Chat.objects.get(pk=self.chat)
        except:
            first_user = Chat.objects.filter(members=self.author)
            second_user = Chat.objects.filter(members=self.recipient)
            qs1 = Chat.objects.all()
            queryset = qs1.intersection(first_user, second_user)
            if queryset.first():
                self.get_or_create_chat = queryset
            else:
                self.get_or_create_chat = None
        return self.get_or_create_chat

    def create_chat(self):
        if self.get_or_create_chat is None:

            members = UserProfile.objects.filter(
                Q(pk=self.author) | Q(pk=self.recipient)
            )

            self.get_or_create_chat = Chat.objects.create(
                created_at=datetime.now()
            )
            for member in members:
                self.get_or_create_chat.members.add(member)
            self.get_or_create_chat.save()
            return self.get_or_create_chat
        else:
            return self.get_or_create_chat

    def create_message(self):
        try:
            id = self.get_or_create_chat.first().id
        except:
            id = self.get_or_create_chat.id
        chat = Chat.objects.get(pk=id)
        message = MessageToUser.objects.create(
            author=self.author_userprofile_instance,
            text=self.text,
            chat=chat,
            created_at=datetime.now()
        )

        message.save()
        return message

    def run_system(self):
        self.get_chat()
        self.create_chat()
        return self.create_message()
