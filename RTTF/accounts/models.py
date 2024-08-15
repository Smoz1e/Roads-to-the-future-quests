# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class AdditionalQuestion(models.Model):
    question_text = models.TextField()
    correct_answer = models.TextField(default='')

    def __str__(self):
        return self.question_text

class Quest(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    main_question = models.TextField()
    main_question_answer = models.TextField(default='')  # Значение по умолчанию
    additional_questions = models.ManyToManyField(AdditionalQuestion, blank=True)

    def __str__(self):
        return self.title

class QuestAnswer(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    main_question_answer = models.TextField()
    additional_question_answers = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.user} - {self.quest}'

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    quests = models.ManyToManyField(Quest, related_name='users', blank=True)







