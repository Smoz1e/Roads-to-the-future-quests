# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    phone_number = forms.CharField(max_length=15, required=True, label='Номер телефона')

    # Добавляем поле класса
    CLASS_CHOICES = [(str(i), str(i)) for i in range(4, 12)]
    class_user = forms.ChoiceField(choices=CLASS_CHOICES, required=True, label='Класс')

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'class_user', 'username', 'password1', 'password2']
        labels = {
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Повторите пароль',
        }

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

class QuestAnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)

        self.fields['answer'] = forms.CharField(
#            label=question.question_text,
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


