from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from .util import unique_slug_generator

# Question model
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, blank=False, null=False)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    point = models.IntegerField(default=0, blank=False, null=False)
    likedUsers = models.ManyToManyField(User, blank=True, related_name='question_liked_users')
    disLikedUsers = models.ManyToManyField(User, blank=True, related_name='question_disliked_users')

    def __str__(self):
        return self.title

# Each answer model
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=False, null=False)
    point = models.IntegerField(default=0, blank=False, null=False)
    likedUsers = models.ManyToManyField(User, blank=True, related_name='answer_liked_users')
    disLikedUsers = models.ManyToManyField(User, blank=True, related_name='answer_disliked_users')

    def __str__(self):
        return self.question.title

# Slug Generation For Question
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Question)
