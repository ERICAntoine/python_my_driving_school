from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login, name= 'login'),
    path('register/', views.register, name= 'login'),
    path('planning/', views.planning, name= 'login'),
    path('planning/update', views.planningUpdate, name= 'planningUpdate'),

]