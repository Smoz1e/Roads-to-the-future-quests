# accounts/admin.py
from django.contrib import admin
from .models import CustomUser, Quest, AdditionalQuestion

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    ordering = ('-date_joined',)

class AdditionalQuestionInline(admin.TabularInline):
    model = Quest.additional_questions.through
    extra = 1

class QuestAdmin(admin.ModelAdmin):
    list_display = ('title', 'main_question')
    inlines = [AdditionalQuestionInline]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Quest, QuestAdmin)
admin.site.register(AdditionalQuestion)



