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
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)

        self.fields['answer'] = forms.CharField(
            label=question.question_text,
            widget=forms.TextInput(attrs={'placeholder': 'Введите ваш ответ'}),
            required=True
        )

        # Поле для сохранения правильности ответа
        self.is_correct = None
        self.response_text = None

    def set_is_correct(self, is_correct):
        self.is_correct = is_correct

    def set_response_text(self, response_text):
        self.response_text = response_text


