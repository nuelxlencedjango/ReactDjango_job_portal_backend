# urls.py
from django.urls import path, include

from .views import ArtisanProfileViewSet ,ArtisanSearchView


urlpatterns = [
    path('artisans/search/', ArtisanSearchView.as_view(), name='artisan_search'),
    path('api/artisans/search/', ArtisanProfileViewSet.as_view(), name='artisan_search'),
]