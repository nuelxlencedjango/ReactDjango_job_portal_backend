
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

        # Fetch the user's cart
        try:
            cart = Cart.objects.filter(user=request.user)
        except Cart.DoesNotExist:
            # If no cart exists, create a new one
            cart = Cart.objects.create(user=request.user, paid=False)

        # Ensure the cart is unpaid
        if cart:
            # If the cart is paid, create a new unpaid cart
            cart = Cart.objects.create(user=request.user, paid=False)

        # Check or create the cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            artisan=artisan,
            service=service,
            paid=False,
        )

        if not created:
            # If the item already exists, just increment the quantity
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




class PaymentInformationView(APIView):
   #authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tx_ref = request.data.get("tx_ref")
        amount = request.data.get("amount")
       
        status = request.data.get("status", "pending")

        if not all([tx_ref, amount, ]):
            return Response({"detail": "Missing required fields."}, status=400)

        try:
            # Save payment information to the database
            payment_info = PaymentInformation.objects.create(
                user=request.user,
                tx_ref=tx_ref,
                amount=amount,
                status=status,
            )

            return Response(
                {"detail": "Payment information saved.", "id": payment_info.id},
                status=201,
            )
        except Exception as e:
            return Response( {"detail": f"An error occurred: {str(e)}"},
                status=500, )
        











import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status

logger = logging.getLogger(__name__)



from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.conf import settings
import logging
from .models import PaymentInformation, Cart, CartItem

logger = logging.getLogger(__name__)

class PaymentConfirmationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Extract payment details from query parameters (or request data)
        payment_status = request.GET.get('status')  # Use request.data for POST data
        tx_ref = request.GET.get('tx_ref')
        transaction_id = request.GET.get('transaction_id')

        if not all([payment_status, tx_ref, transaction_id]):
            logger.error(f"Missing required parameters: status={payment_status}, tx_ref={tx_ref}, transaction_id={transaction_id}")
            return JsonResponse({"detail": "Missing required parameters."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Find the payment by tx_ref
            payment_info = get_object_or_404(PaymentInformation, tx_ref=tx_ref)

            # Update payment status and transaction ID
            payment_info.status = payment_status
            payment_info.transaction_id = transaction_id
            payment_info.save()

            if payment_status == "successful":
                # Get the unpaid cart for the user (if more than one, choose the first one)
                cart = Cart.objects.filter(user=payment_info.user, paid=False).first()

                if not cart:
                    logger.error(f"Cart not found or already paid for user: {payment_info.user}")
                    return JsonResponse({"detail": "Cart not found or already paid."}, status=status.HTTP_404_NOT_FOUND)

                # Mark the cart and items as paid
                cart.paid = True
                cart.save()

                # Update items in the cart to paid status
                CartItem.objects.filter(cart=cart).update(paid=True)

                # Redirect to the frontend success page with query parameters
                frontend_url = f"{settings.FRONTEND_URL}/payment-confirmation?status=success&tx_ref={tx_ref}&transaction_id={transaction_id}"
                return redirect(frontend_url)

            else:
                # Redirect to the frontend failure page with query parameters
                frontend_url = f"{settings.FRONTEND_URL}/payment-confirmation?status=failed&tx_ref={tx_ref}&transaction_id={transaction_id}"
                return redirect(frontend_url)

        except PaymentInformation.DoesNotExist:
            logger.error(f"PaymentInformation not found for tx_ref: {tx_ref}")
            return JsonResponse({"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            logger.error(f"Cart not found for user or cart already paid for tx_ref: {tx_ref}")
            return JsonResponse({"detail": "Cart not found or already paid."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(f"An error occurred during payment confirmation: {str(e)}")
            return JsonResponse({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# views.py
from .serializers import TransactionSerializer

class PaymentDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        # Save payment details to the Transaction model
        transaction = Transaction.objects.create(
            user=user,
            tx_ref=data.get("tx_ref"),
            amount=data.get("amount"),
            status=data.get("status", "Pending"),
            transaction_id=data.get('id')
        )

        # If payment is successful, update the cart and cart items
        if data.get("status") == "Successful":
            cart = Cart.objects.filter(user=user, paid=False).first()
            if cart:
                cart.paid = True
                cart.save()
                cart.items.update(paid=True)  # Mark all cart items as paid

        # Return both a success message and the transaction data
        serializer = TransactionSerializer(transaction)
        return Response(
            {
                "message": "Payment details saved successfully.",
                "transaction": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )





        


class PaymentDetailsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.user
        data = request.data

        # Save payment details to the Transaction model
        transaction = Transaction.objects.create(
            user=user,
            tx_ref=data.get("tx_ref"),
            amount=data.get("amount"),
            status=data.get("status", "Pending"),
            transaction_id=data.get('transaction_id')
        )

        # If payment is successful, update the cart and cart items
        if data.get("status") == "Successful":
            cart = Cart.objects.filter(user=user, paid=False).first()
            if cart:
                cart.paid = True
                cart.save()
                cart.items.update(paid=True)  # Mark all cart items as paid

        # Return both a success message and the transaction data
        serializer = TransactionSerializer(transaction)
        return Response(
            {
                "message": "Payment details saved successfully.",
                "transaction": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )




