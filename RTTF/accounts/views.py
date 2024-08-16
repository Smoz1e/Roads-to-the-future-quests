# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegisterForm, UserLoginForm, QuestAnswerForm
from .models import CustomUser, Quest
from .forms import QuestAnswerForm
from .models import Quest, QuestProgress, Question
import logging
# Домашняя страничка сайта
def home(request):
    return render(request, 'home.html')  # Шаблон домашней страницы

# Профиль пользователя
# accounts/views.py

@login_required
def profile(request):
    user = request.user
    quests = Quest.objects.all()
    quest_status = []

    for quest in quests:
        quest_progress = QuestProgress.objects.filter(user=user, quest=quest).first()
        if quest_progress:
            if quest_progress.is_completed:
                status = "Пройдено"
            else:
                status = "Не пройдено"
        else:
            status = "Нет данных"
        quest_status.append((quest, status))

    return render(request, 'accounts/profile.html', {
        'user': user,
        'quest_status': quest_status,
    })


# Регистрация
class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)
    
# Авторизация
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')  # Перенаправляем на профиль пользователя
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Детали квеста
logger = logging.getLogger(__name__)

# views.py
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quest, QuestProgress, Question
from .forms import QuestAnswerForm

logger = logging.getLogger(__name__)

@login_required
def quest_detail(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    user = request.user
    quest_progress, created = QuestProgress.objects.get_or_create(user=user, quest=quest)
    
    # Получение сохраненных ответов из сессии
    saved_answers = request.session.get(f'saved_answers_{quest_id}', {})
    correct_answers_count = request.session.get(f'correct_answers_count_{quest_id}', 0)

    if request.method == 'POST':
        if 'restart' in request.POST:
            # Логирование для отладки
            logger.debug(f"User {user.id} нажал 'Начать заново' для квеста {quest_id}")
            
            # Если пользователь нажал "Начать заново", очищаем сессию и прогресс квеста
            request.session.pop(f'saved_answers_{quest_id}', None)
            request.session.pop(f'correct_answers_count_{quest_id}', None)
            quest_progress.is_completed = False
            quest_progress.save()
            
            # Логирование для подтверждения сброса
            logger.debug(f"Прогресс для квеста {quest_id} у пользователя {user.id} был сброшен")
            
            return redirect('quest_detail', quest_id=quest_id)
        
        question_id = request.POST.get('question_id')
        question = get_object_or_404(Question, pk=question_id)

        form = QuestAnswerForm(request.POST, question=question)

        if form.is_valid():
            user_answer = form.cleaned_data['answer'].strip().lower()
            correct_answer = question.correct_answer.strip().lower()

            if user_answer == correct_answer:
                form.set_is_correct(True)
                form.set_response_text(question.success_message or 'Верно!')
                correct_answers_count += 1
            else:
                form.set_is_correct(False)
                form.set_response_text('Неверно, попробуйте еще раз.')

            # Сохраняем результат в сессию
            saved_answers[str(question.id)] = {
                'answer': user_answer,
                'is_correct': form.is_correct,
                'response_text': form.response_text,
            }
            request.session[f'saved_answers_{quest_id}'] = saved_answers
            request.session[f'correct_answers_count_{quest_id}'] = correct_answers_count

            # Проверяем, пройдены ли все вопросы
            if correct_answers_count == quest.questions.count():
                quest_progress.is_completed = True
                quest_progress.save()
                request.session[f'quest_completed_{quest_id}'] = True
            else:
                quest_progress.is_completed = False
                quest_progress.save()

        forms = []
        for question in quest.questions.all():
            form_key = str(question.id)
            form_initial = {
                'answer': saved_answers.get(form_key, {}).get('answer', ''),
            }
            form = QuestAnswerForm(initial=form_initial, question=question)
            form.set_is_correct(saved_answers.get(form_key, {}).get('is_correct'))
            form.set_response_text(saved_answers.get(form_key, {}).get('response_text'))
            forms.append((question, form))

    else:
        forms = []
        for question in quest.questions.all():
            form_key = str(question.id)
            form_initial = {
                'answer': saved_answers.get(form_key, {}).get('answer', ''),
            }
            form = QuestAnswerForm(initial=form_initial, question=question)
            form.set_is_correct(saved_answers.get(form_key, {}).get('is_correct'))
            form.set_response_text(saved_answers.get(form_key, {}).get('response_text'))
            forms.append((question, form))

    return render(request, 'accounts/quest_detail.html', {
        'quest': quest,
        'forms': forms,
        'quest_progress': quest_progress,
    })

















