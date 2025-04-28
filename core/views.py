from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import HealthProgramForm
from .forms import ClientForm
from .forms import EnrollmentForm 
from .models import Client,Enrollment,HealthProgram
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import ClientProfileSerializer,HealthProgramSerializer, ClientSerializer


# -------------------- Web Application Views --------------------

# Home page view
def home(request):
    return render(request, 'home.html')

# User registration view
def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 👈 redirect to login instead of dashboard
    return render(request, 'register.html', {'form': form})

# User login view
def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html', {'form': form})

# Dashboard view (requires login)
@login_required
def dashboard(request):
    # Fetch counts for clients, programs, and enrollments
    clients_count = Client.objects.count()
    programs_count = HealthProgram.objects.count()
    enrollments_count = Enrollment.objects.count()

    return render(request, 'dashboard.html', {
        'clients_count': clients_count,
        'programs_count': programs_count,
        'enrollments_count': enrollments_count
    })

# View to create a health program
def create_health_program(request):
    form = HealthProgramForm()
    if request.method == 'POST':
        form = HealthProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Health program created successfully!')
            return redirect('dashboard')
    return render(request, 'create_program.html', {'form': form})

# View to register a new client
def register_client(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client registered successfully!')
            return redirect('dashboard')
    return render(request, 'register_client.html', {'form': form})

# View to enroll a client in health programs
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

# View to search for clients
def search_clients(request):
    query = request.GET.get('q', '')  # Default to an empty string if no query is provided
    if query:
        # Filter clients by name or contact using Q objects
        clients = Client.objects.filter(
            Q(name__icontains=query) | Q(contact__icontains=query)
        )
    else:
        clients = Client.objects.all()   # Return all clients if no query is provided
    return render(request, 'search_clients.html', {'clients': clients, 'query': query})

#def view_clients(request):
    #clients = Client.objects.all()
    #return render(request, 'view_clients.html', {'clients': clients})


# View to display a client's profile
def client_profile(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    enrollments = Enrollment.objects.filter(client=client).select_related('program')
    
    return render(request, 'client_profile.html', {
        'client': client,
        'enrollments': enrollments,
    })


# -------------------- API Views --------------------

# API to create a health program
@api_view(['POST'])
def create_health_program_api(request):
    serializer = HealthProgramSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# API to register a client
@api_view(['POST'])
def register_client_api(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# API to enroll a client in programs
@api_view(['POST'])
def enroll_client_api(request):
    client_id = request.data.get('client_id')
    program_ids = request.data.get('program_ids', [])
    print(f"Client ID: {client_id}, Program IDs: {program_ids}")  

    # Check if the client exists
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found'}, status=404)

    # Enroll the client in the specified programs
    enrollments = []
    for program_id in program_ids:
        try:
            program = HealthProgram.objects.get(id=program_id)
            enrollment = Enrollment.objects.create(client=client, program=program)
            enrollments.append(enrollment)
            print(f"Enrolled in Program ID: {program_id}")  # Debug statement
        except HealthProgram.DoesNotExist:
            return Response({'error': f'Program with id {program_id} not found'}, status=404)

    return Response({'message': 'Client enrolled successfully!'}, status=201)

# API to search for clients
@api_view(['GET'])
def search_clients_api(request):
    query = request.GET.get('q', '')
    clients = Client.objects.filter(Q(name__icontains=query) | Q(contact__icontains=query))
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

# API to fetch a client's profile
@api_view(['GET'])
def client_profile_api(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found'}, status=404)

    serializer = ClientProfileSerializer(client)
    return Response(serializer.data)

