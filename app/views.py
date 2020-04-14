from django.shortcuts import render, HttpResponse
from .models import Users, Planning, Role
from django.template import loader
from django.contrib.auth.hashers import make_password, check_password

from .forms import LoginForm, RegisterForm



# Create your views here.

def index(request):
    template = loader.get_template('base.html')
    context = {
        "toot": 'toto'
    }
    return HttpResponse(template.render(context,request))

def detail(request, users_id):
    response = "You're looking at the results of user %s."
    return HttpResponse(response % users_id)

def login(request):
    template = loader.get_template('registration/login.html')
    context = { 'form': LoginForm }
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            password = request.POST.get('password')
            email = request.POST.get('email')
            user = Users.objects.get(email=email)
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
            if not Users.objects.filter(email=email).exists():
                user = Users(firstname=firstname, lastname=lastname,email=email,password=make_password(password),role=Role.objects.get(id=role))
                user.save()
        context['form'] = form 
    return render(request, 'registration/register.html', context)