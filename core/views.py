from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import HealthProgramForm
from django.contrib import messages
from .forms import ClientForm
from .forms import EnrollmentForm 
from .models import Client,Enrollment,HealthProgram
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
    clients_count = Client.objects.count()
    programs_count = HealthProgram.objects.count()
    enrollments_count = Enrollment.objects.count()

    return render(request, 'dashboard.html', {
        'clients_count': clients_count,
        'programs_count': programs_count,
        'enrollments_count': enrollments_count
    })

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
            client = form.cleaned_data['client']
            programs = form.cleaned_data['program']
            for program in programs:
                Enrollment.objects.create(client=client, program=program)
            messages.success(request, 'Client enrolled successfully into selected programs!')
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

#def view_clients(request):
    #clients = Client.objects.all()
    #return render(request, 'view_clients.html', {'clients': clients})

def client_profile(request, client_id):
    # Fetch the client by ID
    client = get_object_or_404(Client, id=client_id)
    
    # Fetch the programs the client is enrolled in
    enrollments = Enrollment.objects.filter(client=client).select_related('program')
    
    return render(request, 'client_profile.html', {
        'client': client,
        'enrollments': enrollments,
    })