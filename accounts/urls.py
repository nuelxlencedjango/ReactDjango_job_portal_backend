from django.urls import path
from accounts.views import *






urlpatterns = [
   path('register-artisan/', ArtisanUserCreateView.as_view(), name='register-artisan'),
]




