
from django.shortcuts import render
from rest_framework import generics, serializers, status,permissions
#from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView
#from .serializers import CartSerializer, CartItemSerializer,CheckoutSerializer
from django.utils.crypto import get_random_string
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import *
from acct.models import CustomUser, ArtisanProfile,EmployerProfile
from .serializers import *
from django.db import transaction
import json

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# Create your views here.
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404, redirect


from django.http import JsonResponse

from django.conf import settings
import uuid
import requests




#BASE_URL = settings.FRONTEND_URL  
 

class VerifyTokenView(APIView):
    def post(self, request):
        token = request.data.get("token")
        try:
            # Validate token
            UntypedToken(token)
            return Response({"valid": True})
        except (InvalidToken, TokenError):
            return Response({"valid": False}, status=400)




class CheckArtisanInCartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, artisan_email):
        # Check if the user is logged in (Authenticated)
        if request.user:
            user = request.user
            try:
                # Get the user's cart
                cart = Cart.objects.filter(user=user).first()
                

                # Check if the artisan is in the user's cart by checking CartItem
               
                artisan_in_cart = CartItem.objects.filter(cart=cart, artisan__user__email=artisan_email,
                                                          paid =False).first()

                # Return the response based on whether the artisan is in the cart or not
                if artisan_in_cart:
                    return Response({'in_cart': True}, status=200)
                else:
                    return Response({'in_cart': False}, status=200)

            except Cart.DoesNotExist:
                # If no cart exists for the user, return false
                return Response({'in_cart': False}, status=200)

        else:
            # If the user is not logged in, return false (no cart)
            return Response({'in_cart': False}, status=200)








class JobDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the current logged-in user (employer)
        user = request.user
        if not user:
            return Response({"error": "User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)

        job_data = request.data
        job_data['employer'] = user.id  # Set the employer to the logged-in user ID (manually or via the request)

        # Use the serializer to validate the data
        serializer = JobDetailsSerializer(data=job_data)
        if serializer.is_valid():
            # Create the JobDetails instance from the validated data
            job_details = serializer.save()  # This will handle creation using the validated data

            # After successful creation, serialize the created JobDetails and return it
            job_details_serialized = JobDetailsSerializer(job_details)
            return Response(job_details_serialized.data, status=status.HTTP_201_CREATED)

        # If validation fails, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Ensure the user is an employer
        if not request.user.is_employer:
            return Response(
                {"error": "Only employers can add items to the cart."},
                status=status.HTTP_403_FORBIDDEN,
            )

        artisan_email = request.data.get("artisan_email")

        if not artisan_email:
            return Response(
                {"error": "Artisan email is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            artisan = ArtisanProfile.objects.get(user__email=artisan_email)
            service = artisan.service
        except ArtisanProfile.DoesNotExist:
            return Response(
                {"error": "Artisan not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Fetch the user's unpaid cart or create a new one
        try:
            cart = Cart.objects.get(user=request.user, paid=False)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user, paid=False)

        # Check or create the cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            artisan=artisan,
            service=service,
            paid=False,
            defaults={'quantity': 1}  # Default values for creation
        )

        if not created:
            # If the item already exists, increment the quantity
            cart_item.quantity += 1
            cart_item.save()

        return Response(
            {"message": "Item added to cart successfully."}, status=status.HTTP_201_CREATED
        )



class CheckoutView(APIView): 
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type != 'employer':
            return Response({"detail": "User is not an employer."}, status=403)
        
        try:
            carts = Cart.objects.filter(user=user, paid=False)
            serializer = CartSerializer(carts, many =True)
            return Response(
                {"cart": serializer.data,
                "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,},
                },status=200,
                )
        except Cart.DoesNotExist:
            return Response(
        {
            "cart": "Your cart is empty.",
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
        },
        status=200,
    )
       
    def delete(self, request, pk):
        """
        Remove a specific item from the cart.
        """
        try:
            # Fetch the cart of the logged-in user
            cart = Cart.objects.get(user=request.user, paid=False)
            
            # Ensure the cart item exists in the user's cart
            cart_item = CartItem.objects.get(pk=pk, cart=cart,paid =False)
            cart_item.delete()  # Remove the cart item
            
            return Response({"detail": "Cart item removed successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)















import requests









import logging


logger = logging.getLogger(__name__)

class InitiatePayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_anonymous:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Log the incoming request data
            logger.info(f"Request Data: {request.data}")
            logger.info(f"Request Headers: {request.headers}")


            # the user has either an EmployerProfile or ArtisanProfile
            user = request.user
            phone_number = None
            
            # Check if the user is an employer and get phone number from EmployerProfile
            if hasattr(user, 'employerprofile'):  # EmployerProfile
                phone_number = user.employerprofile.phone_number

            # If no phone number found, return an error
            if not phone_number:
                return Response({'error': 'Phone number not found for this user'}, status=status.HTTP_400_BAD_REQUEST)

            # Proceed with your payment logic here
            reference = str(uuid.uuid4())
            cart_code = request.data.get('cart_code')
            cart = Cart.objects.get(cart_code=cart_code)
            total_amount = request.data.get('totalAmount')
            currency = "NGN"
            redirect_url = f"{settings.FRONTEND_URL}/payment-confirmation/" 

            # Create transaction details
            transaction = TransactionDetails.objects.create(
                tx_ref=reference,
                cart=cart,
                total_amount=total_amount,
                currency=currency,
                user=user,
                status="Pending",
            )

            flutterwave_payload = {
                'tx_ref': reference,
                'amount': str(total_amount),
                "currency": currency,
                "redirect_url": redirect_url,
                "customer": {
                    'email': user.email,
                    "name": f"{user.first_name} {user.last_name}",
                    "phone_number": phone_number  
                },
                "customizations": {
                    "title": "Payment for I-wan-wok Services",
                }
            }

          
            headers = {
                   "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
                    "Content-Type": "application/json"
                }


            flutterwave_url = "https://api.flutterwave.com/v3/payments"
            response = requests.post(flutterwave_url, json=flutterwave_payload, headers=headers)

            # Log the Flutterwave API response
            logger.info(f"Flutterwave API Response: {response.status_code}, {response.text}")

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response(response.json(), status=response.status_code)

        except Cart.DoesNotExist:
            logger.error("Cart not found for the provided cart_code")
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request Exception: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Unexpected Error: {str(e)}")
            return Response({'error': 'An unexpected error occurred', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)