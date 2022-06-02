from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


class UserProfile(models.Model):
    """ UserProfile model """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()
    description = models.TextField(max_length=2000, null=True, blank=True)
    rating = models.SmallIntegerField(null=True, blank=True)
    rank = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    """ User`s comment to question or answer """

    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, null=True,
                                     blank=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(
        verbose_name='related object',
        null=True,
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.text[:20]


class Voting(models.Model):
    rating_choice = (
        ('UP_VOTE', 1),
        ('DOWN_VOTE', -1)
    )

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    choose_rating = models.CharField(max_length=50, choices=rating_choice)
    created_at = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, null=True,
                                     blank=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(
        verbose_name='related object',
        null=True,
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.username} - {self.choose_rating}'


class Tag(models.Model):
    """ Tag(s) of question """

    name = models.CharField(verbose_name='Name of tag', max_length=255)

    def __str__(self):
        return f'{self.name}'


class Question(models.Model):
    """ User`s question model """

    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Input your title', max_length=255)
    description = models.TextField(verbose_name='Description of question',
                                   max_length=2000, null=True, blank=True)
    tag = models.ManyToManyField(Tag, verbose_name='User`s tag(s)')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    comment = GenericRelation(Comment)
    voting = GenericRelation(Voting)

    def __str__(self):
        return f'Username: {self.username} - Title: {self.title[:15]}'


class Answer(models.Model):
    """ User`s Answer model """

    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title of answer',
                             max_length=255)
    description = models.TextField(max_length=2000, null=True,
                                   blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    comment = GenericRelation(Comment)
    voting = GenericRelation(Voting)

    def __str__(self):
        return f'Username: {self.username} - Question title: {self.question.title}: Answer title:{self.title[:15]}'

    class Meta:
        verbose_name_plural = 'Answers'



