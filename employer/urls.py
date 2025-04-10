from django.urls import path
from .views import *

from . import views

from django.urls import path
from .views import ExpectedArtisanView


urlpatterns = [
  path('check-artisan/<str:artisan_email>/', CheckArtisanInCartView.as_view(), name='check-artisan'),
   path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
   path('cart-items/', CartItemView.as_view(), name='cart-items'),
   path('cart-item-delete/<int:pk>/', CartItemView.as_view(), name='cart-item-delete'),
   #path('cart-items/', get_cart_items, name='get_cart_items'),
   path('checkout/', CheckoutView.as_view(), name='checkout'),
   path('job-details/', JobDetailsView.as_view(), name='job-details'),

  path('expected-artisan/', ExpectedArtisanView.as_view(), name='expected-artisan'),
   
   path('payment-details/', InitiatePayment.as_view(), name='payment-details'),
   path('payment_confirmation/', ConfirmPayment.as_view(), name='payment_confirmation'),
   
    path('auth/verify-token/', VerifyTokenView.as_view(), name='verify-token'),
 
    #path('employer/last-payment/', LastPaymentView.as_view(), name='last-payment'),
    path('last-payment/', LastPaymentView.as_view(), name='last-payment'),
    path('employer-requests/', ServicesRequestListView.as_view(), name='employer-requests'),
]

