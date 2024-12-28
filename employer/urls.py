from django.urls import path
from .views import *

from . import views


urlpatterns = [
  path('check-artisan/<str:artisan_email>/', CheckArtisanInCartView.as_view(), name='check-artisan'),
 
]
