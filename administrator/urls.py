# urls.py
from django.urls import path, include

from .views import ArtisanSearchView, CompanyListView



urlpatterns = [
    path('artisans/search/', ArtisanSearchView.as_view(), name='artisan_search'),
     path('company-list/', CompanyListView.as_view(), name='company-list'),
   
    
]
