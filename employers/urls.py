from django.urls import path
from .views import *
from . import views


urlpatterns = [
   path('add_employer/', EmployerCreateView.as_view(), name='add_employer'),

]
