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

@login_required
def quest_detail(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    user = request.user
    quest_progress, created = QuestProgress.objects.get_or_create(user=user, quest=quest)
    result = []

    logger.debug(f"QuestProgress for user {user.id} and quest {quest.id}: {quest_progress}")

    if request.method == 'POST':
        form = QuestAnswerForm(request.POST, quest=quest)
        if form.is_valid():
            all_correct = True
            result = []
            for question in quest.questions.all():
                user_answer = form.cleaned_data.get(f'question_{question.id}', '').strip().lower()
                correct_answer = question.correct_answer.strip().lower()
                if user_answer != correct_answer:
                    all_correct = False
                    result.append((question, 'Неверно, попробуйте еще раз.'))
                else:
                    result.append((question, 'Верно!'))

            if all_correct:
                quest_progress.is_completed = True
                quest_progress.save()
                logger.debug(f"Quest completed by user {user.id} for quest {quest.id}")
                result = [("Вы успешно прошли этот квест!", '')]
            else:
                quest_progress.is_completed = False
                quest_progress.save()

    else:
        form = QuestAnswerForm(quest=quest)

    return render(request, 'accounts/quest_detail.html', {
        'quest': quest,
        'form': form,
        'result': result,
        'quest_progress': quest_progress,
    })









