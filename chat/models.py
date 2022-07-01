from django.db import models
from django.conf import settings


class PublicChatRoom(models.Model):
    title = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.title


class PublicChatUserMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_user')
    room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE)
    message = models.TextField(verbose_name='message')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'id: {self.id}, user: {self.user}, message: {self.message}'




