from django.db import models
from django.conf import settings

from userapp.models import UserProfile


class Chat(models.Model):
    members = models.ManyToManyField(UserProfile)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.created_at}'


class MessageToUser(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='author_message')
    text = models.TextField(verbose_name='message')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='message_chat')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'id: {self.id}, Owner: {self.author}, text: {self.text[:30]}'


class PublicChatRoom(models.Model):
    title = models.CharField(max_length=255, unique=True)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='host_user')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return f'{self.id} {self.title}'


class PublicChatUserMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_user')
    room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE)
    message = models.TextField(verbose_name='message')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'id: {self.id}, user: {self.user}, message: {self.message}'