
from django.urls import path
from .views import ArtisanRegistrationView,ListArtisansView

urlpatterns = [
    path('artisan-register/', ArtisanRegistrationView.as_view(), name='artisan_register'),
    path('list-registered-artisans/', ListArtisansView.as_view(), name='list-registered-artisans'),
   
]

