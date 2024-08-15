# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegisterForm, UserLoginForm, QuestAnswerForm
from .models import CustomUser, Quest

# Домашняя страничка сайта
def home(request):
    return render(request, 'home.html')  # Шаблон домашней страницы

# Профиль пользователя
@login_required
def profile(request):
    user = request.user
    quests = Quest.objects.all()  # Получаем все квесты из базы данных
    context = {
        'user': user,
        'quests': quests  # Передаем все квесты в контекст
    }
    return render(request, 'accounts/profile.html', context)

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
@login_required
def quest_detail(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    result = None
    
    if request.method == 'POST':
        form = QuestAnswerForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['answer']
            if user_answer.strip().lower() == quest.correct_answer.strip().lower():
                result = 'Верно!'
            else:
                result = 'Неверно, попробуйте еще раз.'
    else:
        form = QuestAnswerForm()

    return render(request, 'accounts/quest_detail.html', {
        'quest': quest,
        'form': form,
        'result': result,
    })


