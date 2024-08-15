# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    phone_number = forms.CharField(max_length=15, required=True, label='Номер телефона')

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'username', 'password1', 'password2']
        labels = {
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Повторите пароль',
        }

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class QuestAnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        quest = kwargs.pop('quest', None)
        super().__init__(*args, **kwargs)
        if quest:
            for question in quest.questions.all():
                self.fields[f'question_{question.id}'] = forms.CharField(
                    label=question.question_text,
                    widget=forms.Textarea,
                    required=True
                )


