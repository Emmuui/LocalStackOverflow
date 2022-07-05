from django.contrib import admin
from .models import PublicChatRoom, PublicChatUserMessage, MessageToUser


admin.site.register(MessageToUser)
admin.site.register(PublicChatRoom)
admin.site.register(PublicChatUserMessage)
