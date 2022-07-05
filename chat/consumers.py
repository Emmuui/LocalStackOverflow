import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins
from userapp.models import UserProfile
from .serializers import UserSerializer


class UserConsumer(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.PatchModelMixin,
        mixins.UpdateModelMixin,
        mixins.CreateModelMixin,
        mixins.DeleteModelMixin,
        GenericAsyncAPIConsumer,
):

    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
