from django.shortcuts import render, HttpResponse
from .models import Users, Planning, Role
from django.template import loader
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm, RegisterForm
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
    context = {
        "context": "context"
    }
    return render(request, 'planning.html', context)

def login(request):
    template = loader.get_template('registration/login.html')
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
    template = loader.get_template('registration/register.html')
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