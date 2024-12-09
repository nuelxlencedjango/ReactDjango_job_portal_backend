from django.urls import path
from .views import *
from . import views





urlpatterns = [
  # path('register-artisan/', ArtisanUserCreateView.as_view(), name='register-artisan'),

    path('artisan/register/', views.ArtisanRegistrationView.as_view(), name='artisan_register'),
    path('employer/register/', views.EmployerRegistrationView.as_view(), name='employer_register'),
]


