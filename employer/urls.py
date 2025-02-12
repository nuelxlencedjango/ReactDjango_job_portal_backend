from django.urls import path
from .views import *

from . import views


urlpatterns = [
  path('check-artisan/<str:artisan_email>/', CheckArtisanInCartView.as_view(), name='check-artisan'),
   path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
   path('cart-items/', CartItemView.as_view(), name='cart-items'),
   path('cart/<int:pk>/', CartItemView.as_view(), name='cart-item-detail'),
   #path('cart-items/', get_cart_items, name='get_cart_items'),
   path('checkout/', CheckoutView.as_view(), name='checkout'),
   path('job-details/', JobDetailsView.as_view(), name='job-details'),
   
   path('payment-details/', PaymentInformationView.as_view(), name='payment-details'),
   #path('payment_confirmation/', PaymentConfirmationView.as_view(), name='payment_confirmation'),
  path('payment_confirmation/', views.payment_confirmation, name='payment_confirmation'),
   #path('employer-details/', EmployersDetailsView.as_view(), name='employer-details'),
   
    path('auth/verify-token/', VerifyTokenView.as_view(), name='verify-token'),
    #  path('order/', OrderRequestViewPage.as_view(), name='orders'),
]

