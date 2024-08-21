from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),  # Главная страница
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),  # Профиль пользователя
    path('quest/<int:quest_id>/', quest_detail, name='quest_detail'),
    path('lists/', top_user, name='top_user'),
    path('quests/start/<int:quest_id>/', start_quest, name='start_quest'),
    path('quests/complete/<int:quest_id>/', complete_quest, name='complete_quest'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
