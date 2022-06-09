from rest_framework import permissions
from userapp.models import UserProfile


class IsOwnerOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id