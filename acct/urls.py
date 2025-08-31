# users/urls.py
from django.urls import path
from . import views
from .views import *
from .views import FingerprintUploadView
from .views import PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
   
    path('registration/', views.UserRegistrationAndProfileCreation.as_view(), name='registration'),
    path('user-register/', views.UserRegistrationDetailView.as_view(), name='user-register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    

    path('upload-fingerprint/<int:artisan_id>/', FingerprintUploadView.as_view(), name='upload-fingerprint'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),

     path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]






