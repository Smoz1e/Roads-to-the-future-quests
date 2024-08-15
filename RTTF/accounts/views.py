from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Quest, AdditionalQuestion
from .forms import QuestAnswerForm

#**! Домашняя страничка сайта     
def home(request):
    return render(request, 'home.html')  # Шаблон домашней страницы

#**! Профиль пользователя
@login_required
def profile(request):
    user = request.user
    quests = user.quests.all()  # Получаем все квесты, связанные с пользователем
    context = {
        'user': user,
        'quests': quests
    }
    return render(request, 'accounts/profile.html', context)

#**! Регистрации
class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)
    
#**! Авторизация
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')  # Перенаправляем на профиль пользователя
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def quest_detail(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    return render(request, 'accounts/quest_detail.html', {'quest': quest})

