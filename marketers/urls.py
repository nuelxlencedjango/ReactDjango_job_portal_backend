
from django.urls import path
from .views import ArtisanRegistrationView

urlpatterns = [
    path('artisan-register/', ArtisanRegistrationView.as_view(), name='artisan_register'),
    
]


