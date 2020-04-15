from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .models import Users, Planning as Event, Role
from django.template import loader
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm, RegisterForm, PlanningForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login
from django.utils.http import is_safe_url
from django.db.models import Q

# Create your views here.

def index(request):
    template = loader.get_template('base.html')
    context = {
        "toot": 'toto'
    }
    return HttpResponse(template.render(context,request))

def planning(request):
    user = request.user
    events = serializers.serialize('json',Event.objects.all())
    context = { 'form': PlanningForm(user), 'events': events }
    

    if request.method == 'POST':
        form = PlanningForm(user, request.POST)

        if form.is_valid():
            title = request.POST.get('title')
            start = request.POST.get('start')
            end = request.POST.get('end')
            instructor = request.POST.get('instructor')
            student = request.POST.get('student')
            planning = Event()
            planning.title= title
            planning.start = start
            planning.end = end
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

def planningUpdate(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        title = request.POST.get('title')
        start = request.POST.get('start')
        end = request.POST.get('end')
        instructor = request.POST.get('instructor')
        student = request.POST.get('student')
# Event.objects.filter(student=student, start__range=[start, end]) and Event.objects.filter(student=student, end__range=[start, end])
        if Event.objects.filter(instructor=instructor, start__range=[start, end]):
            print('ok')
            return HttpResponse("il y a deja un event à cette endroit ou la date est antérieur");
        else:
            try:
                event = Event.objects.filter(id=id).update(title=title, start=start, end=end, instructor=instructor, student=student)
                if event:
                    return HttpResponse("good");
            except:
                return HttpResponse("il y a deja un event à cette endroit ou la date est antérieur");

def manageAccount(request):
    context = {
        "user": Users.objects.all(),
        "form": RegisterForm
    }
    return render(request, 'manageAccount.html', context)
