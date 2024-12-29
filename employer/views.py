
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
                cart = Cart.objects.get(user=user)

                # Check if the artisan is in the user's cart by checking CartItem
                artisan_in_cart = CartItem.objects.filter(cart=cart, artisan__user__email=artisan_email).exists()

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
        



class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        artisan_email = request.data.get('artisan_email')  

        if not artisan_email:
            return Response({"error": "Artisan email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            artisan = ArtisanProfile.objects.get(user__email=artisan_email) 
            service = artisan.service
        except ArtisanProfile.DoesNotExist:
            return Response({"error": "Artisan not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get or create the cart 
        cart, _ = Cart.objects.get_or_create(user=request.user, paid=False)

        # Check or create the cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, artisan=artisan, service=service)
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()

          
        return Response({"message": "Item added to cart successfully."}, status=status.HTTP_201_CREATED)





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




class CartItemsView(APIView):  
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get all cart items for the logged-in user (Employer) along with user details.
        """
        try:
            # Fetch user details
            user_data = {
                "email": request.user.email,
                "username": request.user.username,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            }

            # Try to retrieve the user's cart
            cart = Cart.objects.filter(user=request.user, paid=False).first()  # `.first()` avoids exceptions if no cart exists
            if cart:
                # Fetch cart items if the cart exists
                cart_items = CartItem.objects.filter(cart=cart)
                cart_items_data = CartItemSerializer(cart_items, many=True).data
            else:
                cart_items_data = []  # Empty list if no cart exists

            # Combine user details and cart items in the response
            response_data = { "user_data": user_data,"cart_items": cart_items_data,}

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """
        Remove a specific item from the cart.
        """
        try:
            cart = Cart.objects.get(user=request.user, paid=False)
            cart_item = CartItem.objects.get(pk=pk, cart=cart)  # Ensure item belongs to this cart
            cart_item.delete()
            
            return Response({"detail": "Cart item removed successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class CartItemsView(APIView):  
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employer = EmployerProfile.objects.filter(user=request.user).first()
        if not employer:
            return Response({"detail": "Employer profile not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_items = CartItem.objects.filter(employer=employer)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response({"cart_items": serializer.data}, status=status.HTTP_200_OK)




class CheckoutView(APIView): 
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CheckoutViewT(APIView): 
    permission_classes = [IsAuthenticated]

    def post(self, request):
        employer = EmployerProfile.objects.filter(user=request.user).first()
        if not employer:
            return Response({"detail": "Employer profile not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_items = CartItem.objects.filter(employer=employer)
        if not cart_items.exists():
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total
        total_amount = sum(item.artisan.pay for item in cart_items)

        # Create an order
        order = Order.objects.create(
            employer=employer,
            total_amount=total_amount,
            purchase_date=now().date(),
        )

        # Optionally, clear cart items after checkout
        cart_items.delete()

        return Response(
            {"order_id": order.id, "total_amount": total_amount},
            status=status.HTTP_201_CREATED,
        )




