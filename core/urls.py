from django.urls import path
from django.contrib.auth.views import LogoutView  # Import LogoutView for user logout functionality
from . import views
from .views import schema_view  # Import schema_view for Swagger and ReDoc API documentation

# Define URL patterns for the application
urlpatterns = [
    # Web application routes
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # User registration page
    path('login/', views.login_view, name='login'),  # User login page
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard for logged-in users
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Logout and redirect to home
    path('create-program/', views.create_health_program, name='create_program'),  # Create a health program
    path('register-client/', views.register_client, name='register_client'),  # Register a new client
    path('enroll-client/', views.enroll_client, name='enroll_client'),  # Enroll a client in health programs
    path('search/', views.search_clients, name='search_clients'),  # Search for clients
    path('client/<int:client_id>/', views.client_profile, name='client_profile'),  # View a client's profile

    # API routes
    path('api/create-program/', views.create_health_program_api, name='create_health_program_api'),  # API to create a health program
    path('api/register-client/', views.register_client_api, name='register_client_api'),  # API to register a client
    path('api/enroll-client/', views.enroll_client_api, name='enroll_client_api'),  # API to enroll a client in programs
    path('api/search-clients/', views.search_clients_api, name='search_clients_api'),  # API to search for clients
    path('api/client/<int:client_id>/', views.client_profile_api, name='client_profile_api'),  # API to view a client's profile

    # Swagger and ReDoc API documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # ReDoc UI
]