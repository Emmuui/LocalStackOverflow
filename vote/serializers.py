from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Vote

CONTENT_TYPES_MODEL = ['question', 'answer', 'comment']


class CreateVoteSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(queryset=ContentType.objects.filter(model__in=CONTENT_TYPES_MODEL),
                                                slug_field='model')
    object_id = serializers.IntegerField(write_only=True)
    user = serializers.CharField(required=False)

    class Meta:
        model = Vote
        fields = ['user', 'content_type', 'object_id', 'choose_rating',
                  'date_created_at']

    def validate(self, attrs):
        try:
            attrs['content_object'] = attrs['content_type'].model_class().objects.get(pk=attrs['object_id'])
        except:
            raise serializers.ValidationError({'object_id': ['Invalid pk "'+str(attrs['object_id'])+'" - object does not exist.']})
        return attrs

