from django.contrib import admin
from .models import PublicChatRoom, PublicChatUserMessage


admin.site.register(PublicChatRoom)
admin.site.register(PublicChatUserMessage)
