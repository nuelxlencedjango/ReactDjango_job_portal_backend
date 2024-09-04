from django.urls import path
from .views import *
from . import views


urlpatterns = [
   path('add_employer/', EmployerCreateView.as_view(), name='add_employer'),
    path('order-request/', OrderRequestCreateView.as_view(), name='order-request'),
      
   
       path('auth/verify-token/', VerifyTokenView.as_view(), name='verify-token'),
      path('order/', OrderRequestViewPage.as_view(), name='orders'),
]
