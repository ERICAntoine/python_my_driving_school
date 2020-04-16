from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login, name= 'login'),
    path('register/', views.register, name= 'login'),
    path('planning/', views.planning, name= 'login'),
    path('planning/update', views.planningUpdate, name= 'planningUpdate'),
    path('planning/delete', views.planningDelete, name= 'planningDelete'),
    path('manageAccount/', views.manageAccount, name= 'manageAccount'),
    path('profile/<int:userID>', views.profile, name= 'profile'),

]