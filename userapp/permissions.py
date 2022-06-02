from rest_framework import permissions
from .models import UserProfile


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user == UserProfile.objects.get(pk=view.kwargs['id'])
