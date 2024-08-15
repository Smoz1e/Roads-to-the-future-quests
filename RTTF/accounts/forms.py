from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import *
from django.forms import formset_factory
from .models import Quest, AdditionalQuestion, QuestAnswer

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
    
class MainQuestionForm(forms.Form):
    main_question_answer = forms.CharField(widget=forms.Textarea, label='Main Question Answer')

class AdditionalQuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        if question:
            self.fields['answer'] = forms.CharField(
                label=question.question_text,
                widget=forms.Textarea,
                required=False
            )

AdditionalQuestionFormSet = formset_factory(AdditionalQuestionForm, extra=0)

class QuestAnswerForm(forms.ModelForm):
    class Meta:
        model = QuestAnswer
        fields = ['main_question_answer']

    def __init__(self, *args, **kwargs):
        quest = kwargs.pop('quest', None)
        super().__init__(*args, **kwargs)
        if quest:
            self.fields['main_question_answer'] = forms.CharField(
                widget=forms.Textarea,
                label='Main Question Answer'
            )
            self.additional_question_formset = AdditionalQuestionFormSet(
                queryset=AdditionalQuestion.objects.filter(id__in=quest.additional_questions.values_list('id', flat=True)),
                prefix='additional_questions'
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            for form in self.additional_question_formset:
                question = AdditionalQuestion.objects.get(question_text=form.cleaned_data.get('question'))
                answer = form.cleaned_data.get('answer')
                if answer:
                    QuestAnswer.objects.create(
                        user=instance.user,
                        quest=instance.quest,
                        main_question_answer=instance.main_question_answer,
                        additional_question_answers={question.id: answer}
                    )
        return instance

