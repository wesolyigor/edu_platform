from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.user_profile, name='profile'),
]
