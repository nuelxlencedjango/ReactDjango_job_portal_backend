# urls.py
from django.urls import path, include

from .views import ArtisanSearchView2 ,ArtisanSearchView


urlpatterns = [
    path('artisans/search/', ArtisanSearchView.as_view(), name='artisan_search'),
    path('artisans/search/', ArtisanSearchView2.as_view(), name='artisan_search2'),
    
]
