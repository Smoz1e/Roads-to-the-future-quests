from django.contrib import admin
from .models import CustomUser, Quest, Question, QuestProgress

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone_number')

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quest', 'question_text', 'correct_answer')

@admin.register(QuestProgress)
class QuestProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'quest', 'is_completed')
    list_filter = ('is_completed', 'user', 'quest')
