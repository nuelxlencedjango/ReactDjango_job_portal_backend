
from django.urls import path
from .views import *



#app_name = 'api'


urlpatterns = [
    path('', ServiceListView.as_view(), name='home'),
    path('industry-list/', IndustryListView.as_view(), name='industry-list'),
    path('location-list/', AreaListView.as_view(), name='location-list'),

    path('artisans-by-service/<str:service_title>/', ArtisansByServiceView.as_view(), name='artisans-by-service'),

    path('profession-list/', ServiceListView.as_view(), name='profession-list'),
    path('artisans-search/', ArtisanSearchListView.as_view(), name='artisans-search'),

  

  
]
