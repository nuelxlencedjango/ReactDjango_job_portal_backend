# users/urls.py
from django.urls import path
from . import views
from .views import *
from .views import FingerprintUploadView

urlpatterns = [
   
    path('registration/', views.UserRegistrationAndProfileCreation.as_view(), name='registration'),
    path('user-register/', views.UserRegistrationDetailView.as_view(), name='user-register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    

    path('upload-fingerprint/<int:artisan_id>/', FingerprintUploadView.as_view(), name='upload-fingerprint'),
   
]


