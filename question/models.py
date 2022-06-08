from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from userapp.models import UserProfile
from vote.models import Vote


class Tag(models.Model):
    """ Tag(s) of question """

    name = models.CharField(verbose_name='Name of tag', max_length=255)

    def __str__(self):
        return f'{self.name}'


class Comment(models.Model):
    """ User`s comment to question or answer """

    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(max_length=1500)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
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


class Question(models.Model):
    """ User`s question model """

    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Input your title', max_length=255)
    description = models.TextField(verbose_name='Description of question',
                                   max_length=2000, null=True, blank=True)
    tag = models.ManyToManyField(Tag, verbose_name='User`s tag(s)', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    comment = GenericRelation(Comment)
    voting = GenericRelation(Vote)

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
    voting = GenericRelation(Vote)

    def __str__(self):
        return f'Username: {self.username} - Question title: {self.question.title}: Answer title:{self.title[:15]}'

    class Meta:
        verbose_name_plural = 'Answers'

