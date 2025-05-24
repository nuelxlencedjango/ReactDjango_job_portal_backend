
from django.urls import path
from .views import ArtisanRegistrationView,MarketerArtisansListView

urlpatterns = [
    path('artisan-register/', ArtisanRegistrationView.as_view(), name='artisan_register'),
    path('list-registered-artisans/', MarketerArtisansListView.as_view(), name='list-registered-artisans'),
   
]

