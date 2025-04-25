from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import HealthProgramForm
from django.contrib import messages
from .forms import ClientForm
from .forms import EnrollmentForm 
from .models import Client
from django.db.models import Q

def home(request):
    return render(request, 'home.html')

def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 👈 redirect to login instead of dashboard
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def create_health_program(request):
    form = HealthProgramForm()
    if request.method == 'POST':
        form = HealthProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Health program created successfully!')
            return redirect('dashboard')
    return render(request, 'create_program.html', {'form': form})

def register_client(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client registered successfully!')
            return redirect('dashboard')
    return render(request, 'register_client.html', {'form': form})

def enroll_client(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client enrolled successfully!')
            return redirect('dashboard')
    else:
        form = EnrollmentForm()

    return render(request, 'enroll_client.html', {'form': form})

def search_clients(request):
    query = request.GET.get('q', '')  # Default to an empty string if no query is provided
    if query:
        # Use Q objects to filter by name or contact with an OR condition
        clients = Client.objects.filter(
            Q(name__icontains=query) | Q(contact__icontains=query)
        )
    else:
        # If no query, return all clients
        clients = Client.objects.all()
    return render(request, 'search_clients.html', {'clients': clients, 'query': query})