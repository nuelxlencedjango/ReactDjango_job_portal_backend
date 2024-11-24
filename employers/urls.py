from django.urls import path
from .views import *

from . import views


urlpatterns = [
   path('add_employer/', EmployerCreateView.as_view(), name='add_employer'),
    path('order-request/', OrderRequestCreateView.as_view(), name='order-request'),

   
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
      path('cart-items/', CartItemsView.as_view(), name='cart-items'),
    path('cart/<int:pk>/', CartItemsView.as_view(), name='cart-item-detail'),

     path('check-artisan/<str:email>/', CheckArtisanInCartView.as_view(), name='check-artisan'),
 
       path('auth/verify-token/', VerifyTokenView.as_view(), name='verify-token'),
      path('order/', OrderRequestViewPage.as_view(), name='orders'),
]


