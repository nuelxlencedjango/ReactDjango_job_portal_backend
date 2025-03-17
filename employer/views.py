
from django.shortcuts import render
from rest_framework import generics, serializers, status,permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from django.utils.crypto import get_random_string
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import *
from acct.models import  ArtisanProfile,EmployerProfile
from .serializers import *
#from django.db import transaction

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.shortcuts import get_object_or_404, redirect
import os 
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from django.conf import settings
import uuid
import requests

from decimal import Decimal


from django.db import transaction

import string
from django.utils import timezone
 

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
        job_data['employer'] = user.id 

        logger.info(f"Request responses: {job_data}")

        # Use the serializer to validate the data
        serializer = JobDetailsSerializer(data=job_data)
        logger.info(f"serializers: {serializer}")

        if serializer.is_valid():
            # Create the JobDetails instance from the validated data
            job_details = serializer.save()  

            logger.info(f" job details: {job_details}")
            # After successful creation, serialize the created JobDetails and return it
            job_details_serialized = JobDetailsSerializer(job_details)

            logger.info(f"job details serializerss: {job_details_serialized}")
            return Response(job_details_serialized.data, status=status.HTTP_201_CREATED)

        # If validation fails, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class AddToCartView1(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Ensure the user is an employer
        if not request.user.is_employer:
            return Response(
                {"error": "Only employers can add  to the cart."},
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
            defaults={'quantity': 1}  
        )

        if not created:
            # If the item already exists, increment the quantity
            cart_item.quantity += 1
            cart_item.save()

        return Response(
            {"message": "Item added to cart successfully."}, status=status.HTTP_201_CREATED
        )



class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Ensure the user is an employer
        if not request.user.is_employer:
            return Response(
                {"error": "Only employers can add to the cart."},
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
        cart, created = Cart.objects.get_or_create(user=request.user, paid=False)

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
        
        secret_key = os.getenv('FLUTTERWAVE_PUBLIC_KEY')

        AUTH_COOKIE_DOMAIN=os.getenv('AUTH_COOKIE_DOMAIN')
        DATABASE_USER = os.getenv('DATABASE_USER')
        API_KEY=os.getenv('API_KEY')
        DATABASE_PASSWORD =os.getenv('DATABASE_PASSWORD')
        FLUTTERWAVE_PUBLIC_KEY =os.getenv('FLUTTERWAVE_PUBLIC_KEY')

        print(f"FLUTTERWAVE_SECRET_KEY: {secret_key}")
        
        try:
            carts = Cart.objects.filter(user=user, paid=False)
            serializer = CartSerializer(carts, many =True)
            return Response( {"cart": serializer.data, "user": { "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,},
                "secret_keys": secret_key,
                'AUTH_COOKIE_DOMAIN:':AUTH_COOKIE_DOMAIN,
                'DATABASE_USER': DATABASE_USER,
                'API_KEY_cloudinary':API_KEY,
                'password_database':DATABASE_PASSWORD,
                'FLUTTERWAVE_PUBLIC_KEY':FLUTTERWAVE_PUBLIC_KEY,
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








import logging


logger = logging.getLogger(__name__)

class InitiatePayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        total_amount = request.data.get('totalAmount')
        cart_code = request.data.get('cart_code')
        currency = "NGN"
        reference = str(uuid.uuid4())  
        user = request.user

        # Check if user is authenticated
        if user.is_anonymous:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the cart
            cart = Cart.objects.get(cart_code=cart_code)
        except ObjectDoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        # Validate user profile and phone number
        if not hasattr(user, 'employerprofile') or not user.employerprofile.phone_number:
            return Response({'error': 'User profile or phone number is missing'}, status=status.HTTP_400_BAD_REQUEST)

        # Flutterwave details
        flutterwave_url = "https://api.flutterwave.com/v3/payments"
        #secret_key = os.getenv('FLUTTERWAVE_SECRET_KEY')  
        secret_key = str(os.environ.get('FLUTTERWAVE_SECRET_KEY'))

        payload = {
            'tx_ref': reference,
            'amount': str(total_amount),
            "currency": currency,
            "redirect_url": "https://react-django-job-portal-frontend.vercel.app/payment-confirmation/", 
            "customer": {
                'email': user.email,
                "name": f"{user.first_name} {user.last_name}",
                "phone_number": user.employerprofile.phone_number
            },
            "customizations": {
                "title": "Payment for I-wan-wok Services",
            }
        }

        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json"
        }
        

        try:
            # Save payment details to your database
            payment = TransactionDetails(
                user=user,
                cart=cart,
                currency=currency,
                total_amount=total_amount,
                tx_ref=reference,
                status="pending"
            )
            payment.save()

            # Send the request to Flutterwave API
            response = requests.post(flutterwave_url, json=payload, headers=headers)
            response_data = response.json()
            logger.info(f"Flutterwave secret key:{secret_key}, flutterwave API Response {response_data}")

            if response.status_code == 200:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # If Flutterwave returns an error
                logger.error(f"Flutterwave API Error: {response_data}")
                return Response({'error': response_data.get("message", "Payment initiation failed")}, status=response.status_code)

        except requests.exceptions.RequestException as err:
            # Handle network-related errors
            logger.error(f"Network Error: {err}")
            return Response({'error': 'Payment initiation failed due to network error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as err:
            # Handle other unexpected errors
            logger.error(f"Unexpected Error: {err}")
            return Response({'error': 'Payment initiation failed due to an unexpected error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






logger = logging.getLogger(__name__)






class ConfirmPaymentq23(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_status = request.GET.get('status')
        tx_ref = request.GET.get('tx_ref')
        transaction_id = request.GET.get('transaction_id')

        logger.info(f"Received payment confirmation request: payment_status={payment_status}, tx_ref={tx_ref}, transaction_id={transaction_id}")

        if not payment_status or not tx_ref or not transaction_id:
            logger.error("Missing required query parameters.")
            return Response(
                {'error': 'Missing required query parameters.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if payment_status != "successful":
            logger.warning(f"Payment status is not successful: {payment_status}")
            return Response(
                {'error': 'Payment was not successful'},
                status=status.HTTP_400_BAD_REQUEST
            )

        headers = {"Authorization": f"Bearer {os.getenv('FLUTTERWAVE_SECRET_KEY')}"}
        verify_url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"

        try:
            logger.info(f"Verifying transaction with Flutterwave: {verify_url}")
            response = requests.get(verify_url, headers=headers)
            response_data = response.json()
            logger.info(f"Flutterwave verification response: {response_data}")

            if response_data['status'] == 'success':
                try:
                    logger.info(f"Looking for transaction with tx_ref: {tx_ref}")
                    transaction = TransactionDetails.objects.get(tx_ref=tx_ref)
                    logger.info(f"Transaction found: {transaction}")

                    # Verify payment details
                    logger.info(f"Flutterwave amount: {response_data['data']['amount']}, Transaction amount: {transaction.total_amount}")
                    logger.info(f"Flutterwave currency: {response_data['data']['currency']}, Transaction currency: {transaction.currency}")

                    if (
                        response_data['data']['status'] == "successful"
                        and float(response_data['data']['amount']) == float(transaction.total_amount)
                        and response_data['data']['currency'] == transaction.currency
                    ):
                        # Update transaction details
                        transaction.status = response_data['data']['status']
                        transaction.transaction_id = response_data['data']['id']
                        transaction.flutter_transaction_id = response_data['data']['id']
                        transaction.flutter_transaction_ref_id = response_data['data']['tx_ref']
                        transaction.flutter_app_fee = response_data['data']['app_fee']
                        transaction.flutter_settled_amount = Decimal(response_data['data']['amount_settled'])
                        transaction.ip_address = response_data['data']['ip']
                        transaction.device_fingerprint = response_data['data']['device_fingerprint']

                        # Handle card details (if present)
                        if 'card' in response_data['data']:
                            transaction.card_type = response_data['data']['card']['type']
                            transaction.flutter_card_issuer = response_data['data']['card']['issuer']
                            transaction.first_6digits = response_data['data']['card']['first_6digits']
                            transaction.last_4digits = response_data['data']['card']['last_4digits']
                        else:
                            transaction.card_type = None
                            transaction.flutter_card_issuer = None
                            transaction.first_6digits = None
                            transaction.last_4digits = None

                        # Save the transaction
                        try:
                            transaction.save()
                            logger.info("Transaction saved successfully.")
                        except Exception as e:
                            logger.error(f"Error saving transaction: {str(e)}")
                            return Response(
                                {'error': 'An error occurred while saving the transaction.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )

                        logger.info(f"Transaction status updated to '{response_data['data']['status']}'.")

                        # Get the cart associated with the transaction
                        cart = transaction.cart
                        cart.paid = True
                        cart.save()
                        logger.info("Cart marked as paid.")

                        # Create Order
                        order_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                        order = Order.objects.create(
                            user=cart.user,
                            order_code=order_code,
                            total_price=transaction.total_amount,
                            cart_code=cart.cart_code,
                            status=response_data['data']['status'],  # Use status from Flutterwave
                            paid=True,
                            paid_at=timezone.now(),
                        )
                        logger.info(f"Order created: {order}")

                        # Create OrderItems
                        for cart_item in cart.items.all():
                            OrderItem.objects.create(
                                order=order,
                                artisan=cart_item.artisan,
                                service=cart_item.service,
                                price=cart_item.artisan.pay,
                                total=transaction.total_amount,
                            )
                            logger.info(f"OrderItem created for cart item: {cart_item}")

                        # Delete or archive cart
                        cart.delete()
                        logger.info("Cart deleted.")

                        return Response(
                            {'message': 'Payment Successful, Order Created', 'subMessage': 'You have successfully made payment'},
                            status=status.HTTP_200_OK
                        )
                    else:
                        logger.error("Payment verification failed: Flutterwave response data does not match transaction details.")
                        return Response(
                            {'message': 'Payment Verification Failed', 'subMessage': 'Your payment verification was NOT successful.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except TransactionDetails.DoesNotExist:
                    logger.error(f"Transaction with tx_ref={tx_ref} not found.")
                    return Response(
                        {'error': 'Transaction not found.'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                logger.error(f"Flutterwave payment verification failed: {response_data}")
                return Response(
                    {'message': 'Payment Verification Failed', 'subMessage': 'Your payment verification was NOT successful.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An error occurred while processing the payment.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def last_transaction(request):
    # Fetch the last paid order for the authenticated user
    last_order = Order.objects.filter(user=request.user, paid=True).last()
    
    if last_order:
        serializer = OrderSerializer(last_order)
        return Response(serializer.data)
    else:
        return Response({"message": "No transactions found"}, status=404)
    



class ConfirmPayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_status = request.GET.get('status')
        tx_ref = request.GET.get('tx_ref')
        transaction_id = request.GET.get('transaction_id')

        logger.info(f"Received payment confirmation request: payment_status={payment_status}, tx_ref={tx_ref}, transaction_id={transaction_id}")

        if not payment_status or not tx_ref or not transaction_id:
            logger.error("Missing required query parameters.")
            return Response({'error': 'Missing required query parameters.'},
                status=status.HTTP_400_BAD_REQUEST )

        if payment_status != "successful":
            logger.warning(f"Payment status is not successful: {payment_status}")
            return Response({'error': 'Payment was not successful'},
                status=status.HTTP_400_BAD_REQUEST )

        headers = {"Authorization": f"Bearer {os.getenv('FLUTTERWAVE_SECRET_KEY')}"}
        verify_url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"

        try:
            logger.info(f"Verifying transaction with Flutterwave: {verify_url}")
            response = requests.get(verify_url, headers=headers)
            response_data = response.json()
            logger.info(f"Flutterwave verification response: {response_data}")

            if response_data['status'] == 'success':
                try:
                    transaction_details = TransactionDetails.objects.get(tx_ref=tx_ref)
                    logger.info(f"Transaction found: {transaction_details}")

                    # Verify payment details
                    if (
                        response_data['data']['status'] == "successful"
                        and float(response_data['data']['amount']) == float(transaction_details.total_amount)
                        and response_data['data']['currency'] == transaction_details.currency ):
                        # Start a transaction block
                        with transaction.atomic():
                            logger.info("Updating transaction details...")

                            # Update transaction details
                            transaction_details.status = response_data['data']['status']
                            transaction_details.transaction_id = response_data['data']['id']
                            transaction_details.flutter_transaction_id = response_data['data']['id']
                            transaction_details.flutter_transaction_ref_id = response_data['data']['tx_ref']
                            transaction_details.flutter_app_fee = response_data['data']['app_fee']
                            transaction_details.flutter_settled_amount = Decimal(response_data['data']['amount_settled'])
                            transaction_details.card_type = response_data['data']['card']['type']
                            transaction_details.ip_address = response_data['data']['ip']
                            transaction_details.device_fingerprint = response_data['data']['device_fingerprint']
                            transaction_details.flutter_card_issuer = response_data['data']['card']['issuer']
                            transaction_details.first_6digits = response_data['data']['card']['first_6digits']
                            transaction_details.last_4digits = response_data['data']['card']['last_4digits']

                            # Log before saving
                            logger.info(f"Transaction details before saving: {transaction_details}")
                            transaction_details.save()

                            logger.info(f"Transaction status updated to '{response_data['data']['status']}'.")

                        # Get the cart associated with the transaction
                        cart = transaction_details.cart
                        cart.paid = True
                        cart.save()
                        logger.info("Cart marked as paid.")

                        # Create Order
                        order_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                        order = Order.objects.create(
                            user=cart.user,
                            order_code=order_code,
                            total_price=transaction_details.total_amount,
                            cart_code=cart.cart_code,
                            status=response_data['data']['status'], 
                            paid=True,
                            paid_at=timezone.now(),
                        )
                        logger.info(f"Order created: {order}")

                        # Create OrderItems
                        for cart_item in cart.items.all():
                            OrderItem.objects.create(
                                order=order,
                                artisan=cart_item.artisan,
                                service=cart_item.service,
                                price=cart_item.artisan.pay,
                                total=transaction_details.total_amount,
                            )
                            logger.info(f"OrderItem created for cart item: {cart_item}")

                        # Delete or archive cart
                        #cart.delete()
                        #logger.info("Cart deleted.")

                        return Response(
                            {'message': 'Payment Successful, Order Created', 'subMessage': 'You have successfully made payment'},
                            status=status.HTTP_200_OK
                        )
                    else:
                        logger.error("Payment verification failed: Flutterwave response data does not match transaction details.")
                        return Response(
                            {'message': 'Payment Verification Failed', 'subMessage': 'Your payment verification was NOT successful.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except TransactionDetails.DoesNotExist:
                    logger.error(f"Transaction with tx_ref={tx_ref} not found.")
                    return Response({'error': 'Transaction not found.'},
                        status=status.HTTP_404_NOT_FOUND )
            else:
                logger.error(f"Flutterwave payment verification failed: {response_data}")
                return Response(
                    {'message': 'Payment Verification Failed', 'subMessage': 'Your payment verification was NOT successful.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}", exc_info=True)
            return Response( {'error': 'An error occurred while processing the payment.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR )
