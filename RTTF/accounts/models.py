from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    quests = models.ManyToManyField('Quest', through='QuestProgress', related_name='users', blank=True)

    def __str__(self):
        return self.username

class Quest(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Question(models.Model):
    quest = models.ForeignKey(Quest, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=200)
    image = models.ImageField(upload_to='questions/', blank=True, null=True)  # поле для картинки

    def __str__(self):
        return f'Вопрос: {self.question_text}'

class QuestProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'quest')

    def __str__(self):
        return f'{self.user.username} - {self.quest.title} - {"Пройдено" if self.is_completed else "Не пройдено"}'




















