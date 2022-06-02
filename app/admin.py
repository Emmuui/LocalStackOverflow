from django.contrib import admin
from .models import UserProfile, Tag, Question, Answer, Comment


admin.site.register(UserProfile)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)