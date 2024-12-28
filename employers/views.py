
from django.shortcuts import render
from rest_framework import generics, serializers, status,permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView
from .serializers import CartSerializer, CartItemSerializer,CheckoutSerializer 
from django.utils.crypto import get_random_string
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
#from artisans.models import *
#from accounts.serializers import *
from .models import *
from .serializers import *
from django.db import transaction
import json














class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        artisan_email = request.data.get('artisan_email')  

        if not artisan_email:
            return Response({"error": "Artisan email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            artisan = Artisan.objects.get(user__email=artisan_email) 
            service = artisan.service
        except Artisan.DoesNotExist:
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





class EmployersDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "full_name": f"{user.first_name} {user.last_name}",
            "email": user.email,
            "phone": user.employer_profile.phone_number,  
           # "address": user.profile.address, 
        }
        return Response(data)
    


#checking below

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from uuid import uuid4
#from .models import Order

@api_view(["POST"])
def create_checkout(request):
    try:
        # Extract data from request
        user = request.user
        total_amount = request.data.get("total_amount")
        items = request.data.get("items")
        
        # Generate unique ID for the order
        order_id = str(uuid4())

        # Save order in the database
        order = Order.objects.create(
            user=user,
            order_id=order_id,
            total_amount=total_amount
        )
        for item in items:
            order.items.create(**item)
        
        # Return order_id
        return Response({"order_id": order_id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
   


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now

#from .models import CartItem, Employer
from .serializers import CartItemSerializer


class CartItemsView(APIView):  
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employer = Employer.objects.filter(user=request.user).first()
        if not employer:
            return Response({"detail": "Employer profile not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_items = CartItem.objects.filter(employer=employer)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response({"cart_items": serializer.data}, status=status.HTTP_200_OK)


class CheckoutView(APIView): 
    permission_classes = [IsAuthenticated]

    def post(self, request):
        employer = Employer.objects.filter(user=request.user).first()
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



# end new
class EmployerCreateView(generics.CreateAPIView):
   # queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user_data = self.request.data.get('user', {})

        if not isinstance(user_data, dict):
            raise serializers.ValidationError({'user': 'Invalid user data'})

        user_data['is_employer'] = True
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            try:
                with transaction.atomic():
                    user = user_serializer.save()
                    user.set_password(user_data.get('password', ''))
                    user.save()
                    serializer.save(user=user)
            except Exception as e:
                raise serializers.ValidationError({'detail': f"An error occurred while saving user data: {str(e)}"})
        else:
            raise serializers.ValidationError(user_serializer.errors)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return response
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError as e:
            return Response({'errors': f"Invalid JSON data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'errors': f"An unknown error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class EmployerSearchListView(generics.ListAPIView):
   # queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['employer_profile__location__location', 'industry__name']
    search_fields = ['user__first_name', 'user__last_name']





#job search list
class JobSearchListView(generics.ListAPIView):
   # queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['location', 'job_type', 'industry']
    search_fields = ['title', 'description', 'industry']





from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
#from .models import OrderRequest
from .serializers import OrderRequestSerializer

class OrderRequestCreateView(generics.CreateAPIView):
  #  queryset = OrderRequest.objects.all()
    serializer_class = OrderRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        artisan_id = self.request.data.get('artisan')
        if Artisan.objects.get(id =artisan_id):
            artisan_id = Artisan.objects.get(id =artisan_id)
            service_id  = artisan_id.service

            try:
                artisan = Artisan.objects.get(pk=artisan_id)
                service = Service.objects.get(pk=service_id)
            except (Artisan.DoesNotExist, Service.DoesNotExist):
                raise serializers.ValidationError("Invalid Artisan or Service")

        # Get the authenticated user
            employer = self.request.user.employer

            serializer.save(
                artisan=artisan,
                service=service,
                employer=employer
            )







class OrderRequestViewPage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class VerifyTokenView(APIView):
    def post(self, request):
        token = request.data.get("token")
        try:
            # Validate token
            UntypedToken(token)
            return Response({"valid": True})
        except (InvalidToken, TokenError):
            return Response({"valid": False}, status=400)



class OrderRequestCreateView(generics.CreateAPIView):
   # queryset = OrderRequest.objects.all()
    serializer_class = OrderRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        artisan_id = self.request.data.get('artisan')
        artisan = Artisan.objects.get(id=artisan_id)
        service_id = artisan.service
        employer = self.request.user.employer

        serializer.save(
            artisan=artisan,
            service=service_id,
            employer=employer
        )




#NEW BEGINNING




class CheckArtisanInCartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, artisan_email):
        # Check if the user is logged in (Authenticated)
        if request.user.is_authenticated:
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
        