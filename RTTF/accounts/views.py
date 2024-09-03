# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegisterForm, UserLoginForm, QuestAnswerForm
from .models import CustomUser, Quest, QuestProgress, Question
import logging
from django.utils import timezone


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
                duration = quest_progress.get_duration()
                if duration:
                    # Форматируем время, чтобы отображать его только до секунд
                    duration_formatted = str(duration).split('.')[0]
                    status += f" (Ваш результат: {duration_formatted})"
            else:
                status = "Не пройдено"
        else:
            status = "Нет данных"
        quest_status.append((quest, status))

    return render(request, 'accounts/profile.html', {
        'user': user,
        'quest_status': quest_status,
    })



@login_required
def start_quest(request, quest_id):
    user = request.user
    quest = get_object_or_404(Quest, id=quest_id)

    quest_progress, created = QuestProgress.objects.get_or_create(user=user, quest=quest)

    if not quest_progress.started_at:
        quest_progress.started_at = timezone.now()
        quest_progress.save()

    return redirect('quest_detail', quest_id=quest.id)


@login_required
def complete_quest(request, quest_id):
    user = request.user
    quest = get_object_or_404(Quest, id=quest_id)

    quest_progress, created = QuestProgress.objects.get_or_create(user=user, quest=quest)

    if not quest_progress.is_completed:
        quest_progress.is_completed = True
        quest_progress.completed_at = timezone.now()
        quest_progress.save()

    return redirect('profile')


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
# views.py
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quest, QuestProgress, Question
from .forms import QuestAnswerForm
from django.utils import timezone

logger = logging.getLogger(__name__)

@login_required
def quest_detail(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    user = request.user
    quest_progress, created = QuestProgress.objects.get_or_create(user=user, quest=quest)

    # Если квест начат, но время не установлено, установим его
    if not quest_progress.started_at:
        quest_progress.started_at = timezone.now()
        quest_progress.save()

    # Получение сохраненных ответов из сессии
    saved_answers = request.session.get(f'saved_answers_{quest_id}', {})
    correct_answers_count = request.session.get(f'correct_answers_count_{quest_id}', 0)

    if request.method == 'POST':
        if 'restart' in request.POST:
            logger.debug(f"User {user.id} нажал 'Начать заново' для квеста {quest_id}")
            request.session.pop(f'saved_answers_{quest_id}', None)
            request.session.pop(f'correct_answers_count_{quest_id}', None)
            quest_progress.is_completed = False
            quest_progress.started_at = timezone.now()  # Сбрасываем время начала
            quest_progress.completed_at = None  # Очищаем время завершения
            quest_progress.save()
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
                quest_progress.completed_at = timezone.now()  # Устанавливаем время завершения
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

from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, F


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import QuestProgress, Quest, CustomUser

@login_required
def top_user(request):
    # Получаем класс или статус и название квеста из GET-запроса для фильтрации
    selected_class = request.GET.get('class_user', None)
    selected_quest = request.GET.get('quest_id', None)

    # Получаем записи QuestProgress для всех завершенных квестов
    completed_quests = QuestProgress.objects.filter(is_completed=True).exclude(completed_at__isnull=True)

    # Фильтруем по выбранному классу или статусу, если он задан
    if selected_class:
        completed_quests = completed_quests.filter(user__class_user=selected_class)

    # Фильтруем по выбранному квесту, если он задан
    if selected_quest:
        completed_quests = completed_quests.filter(quest_id=selected_quest)

    # Получаем параметры сортировки из GET-запроса
    sort_by = request.GET.get('sort_by', 'user')  # По умолчанию сортировка по имени пользователя

    # Сортировка по выбранному критерию
    if sort_by == 'quest_title':
        completed_quests = completed_quests.order_by('quest__title')
    elif sort_by == 'user_class':
        completed_quests = completed_quests.order_by('user__class_user')
    else:
        completed_quests = completed_quests.order_by('user__username')

    # Создаем словарь для хранения пользователей и их квестов с временем прохождения
    user_quests = {}

    for progress in completed_quests:
        user = progress.user
        quest = progress.quest
        duration = progress.get_duration()

        if user not in user_quests:
            user_quests[user] = []

        user_quests[user].append((quest.title, duration))

    # Сортируем пользователей по имени пользователя
    sorted_users = sorted(user_quests.items(), key=lambda x: x[0].username.lower())

    return render(request, 'accounts/top_user.html', {
        'sorted_users': sorted_users,
        'sort_by': sort_by,
        'selected_class': selected_class,
        'selected_quest': selected_quest,
        'classes': CustomUser.CLASS_AND_STATUS_CHOICES,  # Передаем возможные классы и статусы в шаблон
        'quests': Quest.objects.all(),  # Передаем все квесты в шаблон для фильтрации
    })















