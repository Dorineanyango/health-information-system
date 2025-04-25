from django.urls import path
from django.contrib.auth.views import LogoutView  # Import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]