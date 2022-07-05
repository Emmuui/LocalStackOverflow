from django.contrib import admin
from .models import PublicChatRoom, PublicChatUserMessage, MessageToUser, Chat


admin.site.register(Chat)
admin.site.register(MessageToUser)
admin.site.register(PublicChatRoom)
admin.site.register(PublicChatUserMessage)
