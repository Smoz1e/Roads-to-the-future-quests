# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class AdditionalQuestion(models.Model):
    question_text = models.TextField()
    correct_answer = models.TextField(default='')

    def __str__(self):
        return self.question_text

class Quest(models.Model):
    title = models.CharField(max_length=200)
    question = models.TextField()  # Вопрос к квесту
    correct_answer = models.CharField(max_length=200, default='default_answer')  # Правильный ответ, добавлен default

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    quests = models.ManyToManyField(Quest, related_name='users', blank=True)









