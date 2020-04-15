from django.shortcuts import render, HttpResponse
from .models import Users, Planning as AddEvent, Role
from django.template import loader
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm, RegisterForm, PlanningForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login
from django.utils.http import is_safe_url


# Create your views here.

def index(request):
    template = loader.get_template('base.html')
    context = {
        "toot": 'toto'
    }
    return HttpResponse(template.render(context,request))

def planning(request):
    user = request.user
    context = { 'form': PlanningForm(user) }

    if request.method == 'POST':
        form = PlanningForm(user, request.POST)

        if form.is_valid():
            title = request.POST.get('title')
            date_start = request.POST.get('date_start')
            date_end = request.POST.get('date_end')
            instructor = request.POST.get('instructor')
            student = request.POST.get('student')
            planning = AddEvent()
            planning.title= title
            planning.date_start = date_start
            planning.date_end = date_end
            planning.instructor = Users.objects.get(id=instructor)
            planning.student = Users.objects.get(id=student)
            planning.save()
        else:
            context['form'] = form 

    return render(request, 'planning.html', context)

def login(request):
    context = { 'form': LoginForm }

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            password = request.POST.get('password')
            email = request.POST.get('email')
            user = authenticate(email=email, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect("/app/planning/")
            else:
                print("Error")

        context['form'] = form 
    return render(request, 'registration/login.html', context)

def register(request):
    context = { 'form': RegisterForm }
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            password = request.POST.get('password')
            email = request.POST.get('email')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            role = request.POST.get('role')
            user = Users.objects.filter(email=email).exists()
            if not user:
                user = Users.objects.create_user(firstname=firstname, lastname=lastname,email=email,password=password,role=Role.objects.get(id=role))
                return redirect("/app/login/")
            else:
                form.add_error("email",'This email address is already in use.')
           
        context['form'] = form 
    return render(request, 'registration/register.html', context)