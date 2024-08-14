from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.forms import AuthenticationForm

#**! Домашняя страничка сайта
def home(request):
    return render(request, 'home.html')  # Шаблон домашней страницы

#**! Профиль пользователя
@login_required
def profile(request):
    return render(request, 'accounts/profile.html')  # Шаблон профиля пользователя

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


