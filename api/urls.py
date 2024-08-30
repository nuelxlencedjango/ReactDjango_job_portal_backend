
from django.urls import path
from .views import *



#app_name = 'api'


urlpatterns = [
    path('', ServiceListView.as_view(), name='home'),
    path('industry-list/', IndustryListView.as_view(), name='industry-list'),

  
]
