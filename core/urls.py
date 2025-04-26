from django.urls import path
from django.contrib.auth.views import LogoutView  # Import LogoutView
from . import views
from .views import schema_view


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

    # API routes
    path('api/create-program/', views.create_health_program_api, name='create_health_program_api'),
    path('api/register-client/', views.register_client_api, name='register_client_api'),
    path('api/enroll-client/', views.enroll_client_api, name='enroll_client_api'),
    path('api/search-clients/', views.search_clients_api, name='search_clients_api'),
    path('api/client/<int:client_id>/', views.client_profile_api, name='client_profile_api'),

    
    # Other URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   
    
]