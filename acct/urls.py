# users/urls.py
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('register/artisan/', views.ArtisanRegistrationView.as_view(), name='artisan-register'),
    path('register/employer/', views.EmployerRegistrationView.as_view(), name='employer-register'),
    path('register/manager/', views.ManagerRegistrationView.as_view(), name='manager-register'),
]


