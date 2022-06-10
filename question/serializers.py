from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Question, Tag, Answer, Comment


CONTENT_TYPES_MODEL = ['question', 'answer']
CONTENT_TYPES_PK = [8, 11]


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class TagCreateView(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class QuestionUpdateSerializer(serializers.ModelSerializer):
    tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                             write_only=True, many=True)
    description = serializers.CharField(required=False)

    class Meta:
        model = Question
        fields = ['title', 'description',
                  'tag']

    def create(self, validated_data):
        tags = validated_data.pop('tag')
        question = Question.objects.create(**validated_data)
        for tag in tags:
            question.tag.add(tag)
        return question


class QuestionSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'description',
                  'tag', 'created_at', 'updated_at']


class CreateQuestionSerializer(serializers.ModelSerializer):
    tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                             write_only=True, many=True)
    description = serializers.CharField(required=False)

    class Meta:
        model = Question
        fields = ['title', 'tag', 'description']

    def create(self, validated_data):
        tags = validated_data.pop('tag')
        question = Question.objects.create(**validated_data)
        for tag in tags:
            question.tag.add(tag)
        return question


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = ['id', 'user', 'title',
                  'description', 'question']


class CreateAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['user', 'title', 'description', 'question']


class CommentSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(queryset=ContentType.objects.filter(model__in=CONTENT_TYPES_MODEL),
                                                slug_field='model')
    object_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

    def validate(self, attrs):
        try:
            attrs['content_object'] = attrs['content_type'].model_class().objects.get(pk=attrs['object_id'])
        except:
            raise serializers.ValidationError({'object_id': ['Invalid pk "'+str(attrs['object_id'])+'" - object does not exist.']})
        return attrs