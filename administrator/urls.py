# urls.py
from django.urls import path, include

from .views import ArtisanSearchView



urlpatterns = [
    path('artisans/search/', ArtisanSearchView.as_view(), name='artisan_search'),
  
   
    
]
