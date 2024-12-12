# users/urls.py
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    #path('artisan-register/', views.ArtisanRegistrationView.as_view(), name='artisan-register'),
    #path('employer-register/', views.EmployerRegistrationView.as_view(), name='employer-register'),
   # path('register/manager/', views.ManagerRegistrationView.as_view(), name='manager-register'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
   
]


