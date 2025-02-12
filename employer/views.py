
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
from django.http import HttpResponseRedirect
from django.urls import reverse






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
        # Ensure the user is an employer
        if not request.user.is_employer:
            return Response({"error": "Only employers can add items to the cart."},
                status=status.HTTP_403_FORBIDDEN )

        artisan_email = request.data.get('artisan_email')  

        if not artisan_email:
            return Response({"error": "Artisan email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            artisan = ArtisanProfile.objects.get(user__email=artisan_email) 
            service = artisan.service
        except ArtisanProfile.DoesNotExist:
            return Response({"error": "Artisan not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create or retrieve the cart for the authenticated user
        cart, _ = Cart.objects.get_or_create(user=request.user, paid=False)

        # Check or create the cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, artisan=artisan, service=service,paid =False,
        )
        
        if not created:
            # If the item already exists, just increment the quantity
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




class CartItemsViewcc(APIView):  
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get all cart items for the logged-in user (Employer) along with user details.
        """
        if not request.user.is_employer:
            return Response({"error": "Only employers can add items to the cart."},
                status=status.HTTP_403_FORBIDDEN )

        try:
            # Fetch user details
            #user_data = CustomUser.objects.get(user = request.user )
            
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




from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartItemsViewkkk(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get all cart items for the logged-in user (Employer) along with user details.
        """
        if not request.user.is_employer:
            return Response({"error": "Only employers can view items in the cart."}, status=status.HTTP_403_FORBIDDEN)

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
                # Serialize the cart with items
                cart_data = CartSerializer(cart).data
                cart_items_data = cart_data['items']  # This already contains serialized items
            else:
                cart_items_data = []  # Empty list if no cart exists

            # Combine user details and cart items in the response
            response_data = {
                "user_data": user_data,
                "cart_items": cart_items_data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """
        Remove a specific item from the cart.
        """
        try:
            # Fetch the cart of the logged-in user
            cart = Cart.objects.get(user=request.user, paid=False)
            
            # Ensure the cart item exists in the user's cart
            cart_item = CartItem.objects.get(pk=pk, cart=cart)
            cart_item.delete()  # Remove the cart item
            
            return Response({"detail": "Cart item removed successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type != 'employer':
            return Response({"detail": "User is not an employer."}, status=403)

        try:
            cart = Cart.objects.get(user=user, paid=False)
            serializer = CartSerializer(cart)
            return Response( 
                { "cart": serializer.data, "user": { "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name, 
                        "email": user.email, },
                },status=200,
                        )
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=404)
        

    def delete(self, request, pk):
        """
        Remove a specific item from the cart.
        """
        try:
            # Fetch the cart of the logged-in user
            cart = Cart.objects.get(user=request.user, paid=False)
            
            # Ensure the cart item exists in the user's cart
            cart_item = CartItem.objects.get(pk=pk, cart__user=cart)
            cart_item.delete()  # Remove the cart item
            
            return Response({"detail": "Cart item removed successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class PaymentInformationView(APIView):
   #authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tx_ref = request.data.get("tx_ref")
        amount = request.data.get("amount")
        #customer_name = request.data.get("customer_name")
        #customer_email = request.data.get("customer_email")
        #customer_phone = request.data.get("customer_phone")
        status = request.data.get("status", "pending")

        if not all([tx_ref, amount, ]):
            return Response({"detail": "Missing required fields."}, status=400)

        try:
            # Save payment information to the database
            payment_info = PaymentInformation.objects.create(
                user=request.user,
                tx_ref=tx_ref,
                amount=amount,
                #customer_name=customer_name,
                #customer_email=customer_email,
                #customer_phone=customer_phone,
                status=status,
            )

            return Response(
                {"detail": "Payment information saved.", "id": payment_info.id},
                status=201,
            )
        except Exception as e:
            return Response(
                {"detail": f"An error occurred: {str(e)}"},
                status=500,
            )
        
        
from django.contrib.auth import authenticate, login




from rest_framework.authtoken.models import Token  


from django.http import JsonResponse



from rest_framework_simplejwt.tokens import AccessToken, TokenError



from django.http import JsonResponse

from rest_framework_simplejwt.tokens import AccessToken, TokenError

import logging

logger = logging.getLogger(__name__)
CustomUser = get_user_model()

def payment_confirmation(request):
    if request.method != 'GET':
        return JsonResponse({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Extract token from query parameters
    token = request.GET.get('token')
    
    if not token:
        return JsonResponse({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Log the token for debugging
        logger.info(f"Received token: {token}")

        # Decode the JWT token
        access_token = AccessToken(token)
        user_id = access_token['user_id']  

        # Log the decoded payload for debugging
        logger.info(f"Decoded token payload: {access_token.payload}")

        # Fetch the user associated with the token
        user = CustomUser.objects.get(id=user_id)
    except TokenError as e:
        logger.error(f"Token error: {e}")
        return JsonResponse({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
    except CustomUser.DoesNotExist:
        logger.error(f"User not found for user_id: {user_id}")
        return JsonResponse({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({"detail": "An error occurred while processing the token."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Extract payment details from query parameters
    payment_status = request.GET.get('status')
    tx_ref = request.GET.get('tx_ref')
    transaction_id = request.GET.get('transaction_id')

    try:
        # Find the payment by tx_ref and user
        payment_info = PaymentInformation.objects.get(tx_ref=tx_ref, user=user)

        # Update payment status and transaction ID
        payment_info.status = payment_status
        payment_info.transaction_id = transaction_id
        payment_info.save()

        if payment_status == "successful":
            # Mark the cart and items as paid
            cart = Cart.objects.get(user=user, paid=False)
            cart.paid = True
            cart.save()

            CartItem.objects.filter(cart=cart).update(paid=True)

            return JsonResponse({
                "detail": "Payment confirmed successfully.",
                "redirect_url": "https://react-frontend.vercel.app/payment-confirmation",
            }, status=status.HTTP_200_OK)

        else:
            return JsonResponse({
                "detail": "Payment was not successful.",
                "redirect_url": "https://react-frontend.vercel.app/payment-confirmation",
            }, status=status.HTTP_400_BAD_REQUEST)

    except PaymentInformation.DoesNotExist:
        return JsonResponse({"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)
    except Cart.DoesNotExist:
        return JsonResponse({"detail": "Cart not found or already paid."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)