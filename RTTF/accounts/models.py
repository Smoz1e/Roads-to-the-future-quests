from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True,  # Обеспечивает уникальность значений в этом поле
        validators=[
            RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Номер телефона должен быть введен в правильном формате.")
        ]
    )
    quests = models.ManyToManyField('Quest', through='QuestProgress', related_name='users', blank=True)

    # Поле для указания класса и статуса пользователя
    CLASS_CHOICES = [(str(i), str(i)) for i in range(4, 12)]  # Классы с 4 по 11
    STATUS_CHOICES = [
        ('student', 'Студент'),
        ('finished', 'Закончил обучение')
    ]
    CLASS_AND_STATUS_CHOICES = CLASS_CHOICES + STATUS_CHOICES

    class_user = models.CharField(max_length=10, choices=CLASS_AND_STATUS_CHOICES, default='5', blank=False, null=False)

    def __str__(self):
        return self.username

class Quest(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

# models.py
class Question(models.Model):
    quest = models.ForeignKey(Quest, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=200)
    image = models.ImageField(upload_to='questions/', blank=True, null=True)  # изображение для вопроса
    success_message = models.TextField(blank=True, null=True)  # текст успешного ответа
    success_image = models.ImageField(upload_to='success_images/', blank=True, null=True)  # изображение успешного ответа
    external_link = models.URLField(blank=True, null=True) #Поле для ссылки на сайт

    def __str__(self):
        return f'Вопрос: {self.question_text}'

from django.utils import timezone
from datetime import timedelta
class QuestProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)  # Время начала квеста
    completed_at = models.DateTimeField(null=True, blank=True)  # Время завершения квеста

    class Meta:
        unique_together = ('user', 'quest')

    def __str__(self):
        return f'{self.user.username} - {self.quest.title} - {"Пройдено" if self.is_completed else "Не пройдено"}'

    def get_duration(self):
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return None





















