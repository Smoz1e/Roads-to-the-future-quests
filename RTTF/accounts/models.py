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

    # Поле для указания класса
    CLASS_CHOICES = [(str(i), str(i)) for i in range(4, 12)]
    class_user = models.CharField(max_length=2, choices=CLASS_CHOICES, blank=False, null=False)

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




















