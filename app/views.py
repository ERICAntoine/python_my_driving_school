from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import JsonResponse, Http404
from django.core import serializers
from .models import Users, Planning as Event, Role
from django.template import loader
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm, RegisterForm, PlanningForm, ProfileForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.utils.http import is_safe_url
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
import json
from datetime import datetime

# Create your views here.

def index(request):
    template = loader.get_template('base.html')
    context = {
        "toot": 'toto'
    }
    return HttpResponse(template.render(context,request))

def planning(request):
    user = request.user
    if user.role.id == 2:
        events = Event.objects.filter(instructor=user.id)
    elif user.role.id == 1:
        events = Event.objects.filter(student=user.id)
    else:
        events = Event.objects.all()

    events = serializers.serialize('json', events)
    context = { 'form': PlanningForm(user), 'events': events }
    

    if request.method == 'POST':
        form = PlanningForm(user, request.POST)

        if form.is_valid():
            id = request.POST.get('id')
            title = request.POST.get('title')
            start = request.POST.get('start')
            end = request.POST.get('end')
            instructor = request.POST.get('instructor')
            student = request.POST.get('student')
            if Event.objects.filter(instructor=instructor,start__range=(start, end)).exclude(id=id) or Event.objects.filter(instructor=instructor, end__range=(start, end)).exclude(id=id):
                form.add_error("start",'Cette date est deja prise par vous ou un autre instructeur.')
                context['form'] = form
                return render(request, 'planning.html', context)
            elif Event.objects.filter(student=student, start__range=(start, end)).exclude(id=id) or Event.objects.filter(student=student, end__range=(start, end)).exclude(id=id):
                form.add_error("end",'Cette date est deja prise par vous ou un autre instructeur.')
                context['form'] = form
                return render(request, 'planning.html', context)
            else:
                planning = Event()
                planning.instructor = Users.objects.get(id=instructor)
                planning.student = Users.objects.get(id=student)
                planning.title = title + " entre Instructeur " + planning.instructor.email + " et Etudiant " + planning.student.email
                planning.start = start
                planning.end = end
                planning.save()
                return redirect("/app/planning/")
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
                if request.user.role.id > 2:
                    return redirect("/app/manageAccount/")
                else:
                    return redirect("/app/login/")
            else:
                form.add_error("email",'This email address is already in use.')
           
        context['form'] = form 
    return render(request, 'registration/register.html', context)

def planningUpdate(request):
    user = request.user
    if user.role.id > 1:
        if request.method == 'POST':
            id = request.POST.get('id')
            title = request.POST.get('title')
            start = request.POST.get('start')
            end = request.POST.get('end')
            instructor = request.POST.get('instructor')
            student = request.POST.get('student')
            if Event.objects.filter(instructor=instructor,start__range=(start, end)).exclude(id=id) or Event.objects.filter(instructor=instructor, end__range=(start, end)).exclude(id=id):
                return bad_request("L'instructor a deja un cours ici")
            elif Event.objects.filter(student=student, start__range=(start, end)).exclude(id=id) or Event.objects.filter(student=student, end__range=(start, end)).exclude(id=id):
                return bad_request("Le student a deja un cours ici")
            else:
                try:
                    event = Event.objects.filter(id=id).update(title=title, start=start, end=end, instructor=instructor, student=student)
                    if event:
                        return HttpResponse("good");
                except:
                    return HttpResponse("il y a deja un event à cette endroit ou la date est antérieur")
    else:
        return Http404("Tu es etudiant !");


def manageAccount(request):
    user = request.user
    if user.role.id == 2:
        context = {
            "users": Event.objects.filter(instructor=user.id),
        }
        print(Event.objects.filter(instructor=user.id))
        return render(request, 'manageAccount.html', context)
    if user.role.id == 3:
        context = {
            "users": Users.objects.all().exclude(role=3),
            "form": RegisterForm
        }
        return render(request, 'manageAccount.html', context)
    elif user.role.id == 4:
        context = {
            "users": Users.objects.all().exclude(role=4),
            "form": RegisterForm
        }
        return render(request, 'manageAccount.html', context)
    else:   
        raise PermissionDenied

def profile(request, userID):
    user = get_object_or_404(Users, pk=userID)
    if user.role.id == 1:
        try:
            events = Event.objects.filter(student=user.id)
        except:
            events = {}
    elif user.role.id == 2:
        try:
            events = Event.objects.filter(instructor=user.id)
        except:
            events = {}
    else: 
        events = {}
    
    events = serializers.serialize('json', events)
    formEvent = PlanningForm(user)
    formProfile = ProfileForm(initial={
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "role" : user.role
    })

    context = {
        "profile": user,
        "formProfile": formProfile,
        "userID": userID,
        "events": events,
        "formEvent": formEvent
    }

    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("/app/profile/"+ str(userID))
    

    return render(request, 'profile.html', context)

def planningDelete(request):
    user = request.user
    if user.role.id > 1:
        if request.method == "POST":
            id = request.POST.get('id')
            try:
                Event.objects.filter(id=id).delete()
                return HttpResponse('good')
            except:
                return bad_request("L'event n'existe pas")
    else:
        return bad_request("L'event n'existe pas")

def profileDelete(request, userID):
    user = request.user
    if user.role.id > 2:
        id = request.POST.get('id')
        try:
            u = Users.objects.get(id=userID)
            u.delete()
            return redirect("/app/manageAccount/")
        except:
            return bad_request("Le profil n'existe pas")
    else:
        raise PermissionDenied

def planningUpdateOther(request, userID):
    user = request.user
    if user.role.id >= 2:
        id = request.POST.get('id')

        if request.method == 'POST':
            try:
                event = Event.objects.get(id=userID)
                event.title = request.POST.get('title')
                event.start = request.POST.get('start')
                event.end = request.POST.get('end')
                event.instructor = request.POST.get('instructor')
                event.student = request.POST.get('student')
                event.save()
                return HttpResponse('good')
            except:
                return bad_request("Le profil n'existe pas")
    else:
        return bad_request("Tu n'a pas les droits")

def bad_request(message):
    response = HttpResponse(json.dumps({'message': message}), content_type='application/json')
    response.status_code = 400
    return response

def logoutAccount(request):
    logout(request)
    return redirect('/app/login')

