from django.urls import path
from django.contrib.auth.views import LogoutView  # Import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('create-program/', views.create_health_program, name='create_program'),
    path('register-client/', views.register_client, name='register_client'),
    path('enroll-client/', views.enroll_client, name='enroll_client'),
    path('search/', views.search_clients, name='search_clients'),
    path('client/<int:client_id>/', views.client_profile, name='client_profile'),
    path('api/client/<int:client_id>/', views.client_profile_api, name='client_profile_api'),
    
]