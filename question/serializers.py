from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Question, Tag, Answer, Comment


CONTENT_TYPES_MODEL = ['question', 'answer']


class TagSerializer(serializers.ModelSerializer):
    """ Tag serializer for CRUD views """
    class Meta:
        model = Tag
        fields = "__all__"


class QuestionUpdateSerializer(serializers.ModelSerializer):
    """ Question serializer for update view  """

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
    """ Question serializer with one additional field for rating """

    tag = TagSerializer(many=True)
    rating = serializers.SerializerMethodField('check_rating')

    class Meta:
        model = Question
        fields = ['id', 'title', 'description',
                  'tag', 'rating', 'created_at', 'updated_at']

    def check_rating(self, question):
        question = Question.objects.get(pk=question.pk)
        positive_rating = question.voting.filter(choose_rating=1).count()
        negative_rating = question.voting.filter(choose_rating=-1).count()
        rating = positive_rating + (negative_rating * -1)
        return rating


class CreateQuestionSerializer(serializers.ModelSerializer):
    """ Question serializer for create view """

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
    """ Answer serializer with one additional field for rating """

    question = QuestionSerializer()
    rating = serializers.SerializerMethodField('check_rating')

    class Meta:
        model = Answer
        fields = ['id', 'user', 'title',
                  'description', 'rating', 'question']

    def check_rating(self, answer):
        answer = Answer.objects.get(pk=answer.pk)
        positive_rating = answer.voting.filter(choose_rating=1).count()
        negative_rating = answer.voting.filter(choose_rating=-1).count()
        rating = positive_rating + (negative_rating * -1)
        return rating


class CreateAnswerSerializer(serializers.ModelSerializer):
    """ Answer serializer for create view """

    class Meta:
        model = Answer
        fields = ['user', 'title', 'description', 'question']


class CommentCreateSerializer(serializers.ModelSerializer):
    """ Comment create serializer  """

    content_type = serializers.SlugRelatedField(queryset=ContentType.objects.filter(model__in=CONTENT_TYPES_MODEL),
                                                slug_field='model')
    object_id = serializers.IntegerField(write_only=True)
    rating = serializers.SerializerMethodField('check_rating')

    class Meta:
        model = Comment
        fields = "__all__"

    def validate(self, attrs):
        try:
            attrs['content_object'] = attrs['content_type'].model_class().objects.get(pk=attrs['object_id'])
        except:
            raise serializers.ValidationError({'object_id': ['Invalid pk "'+str(attrs['object_id'])+'" - object does not exist.']})
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """ Comment serializer with one additional field for rating """

    rating = serializers.SerializerMethodField('check_rating')

    class Meta:
        model = Comment
        fields = ['user', 'text', 'parent',
                  'created_at', 'updated_at', 'rating',
                  'content_type', 'object_id']

    def check_rating(self, comment):
        comment = Comment.objects.get(pk=comment.pk)
        positive_rating = comment.voting.filter(choose_rating=1).count()
        negative_rating = comment.voting.filter(choose_rating=-1).count()
        rating = positive_rating + (negative_rating * -1)
        return rating

