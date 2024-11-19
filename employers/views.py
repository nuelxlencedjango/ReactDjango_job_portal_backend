
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import generics, serializers, status,permissions

from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from artisans.models import *
from accounts.serializers import *
from employers.models import *
from employers.serializers import *
from django.db import transaction
import json


#new logic

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, Artisan

from rest_framework.views import APIView

from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from django.utils.crypto import get_random_string




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cartd(request):
    artisan_id = request.data.get('artisan_id')

    try:
        artisan = Artisan.objects.get(id=artisan_id)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            artisan=artisan
        )

        if created:
            return Response({"message": "Service added to cart successfully"}, status=200)
        else:
            return Response({"message": "Service already in cart"}, status=200)
    except Artisan.DoesNotExist:
        return Response({"error": "Artisan not found"}, status=404)





class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve the cart for the logged-in user."""
        cart, created = Cart.objects.get_or_create(user=request.user, paid=False)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Add an item to the user's cart."""
        artisan_id = request.data.get('artisan')
        service_id = request.data.get('service')
        quantity = request.data.get('quantity', 1)

        if not artisan_id or not service_id:
            return Response({"error": "Artisan and Service are required"}, status=status.HTTP_400_BAD_REQUEST)

        cart, created = Cart.objects.get_or_create(user=request.user, paid=False, defaults={"cart_code": get_random_string(11)})
        item, created = CartItem.objects.get_or_create(cart=cart, artisan_id=artisan_id, service_id=service_id)
        if not created:
            item.quantity += quantity
        item.save()

        return Response({"message": "Item added to cart"}, status=status.HTTP_201_CREATED)

class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        """Remove an item from the cart."""
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user, cart__paid=False)
            item.delete()
            return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)



# end new


class EmployerCreateView(generics.CreateAPIView):
    queryset = Employer.objects.all()
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
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['employer_profile__location__location', 'industry__name']
    search_fields = ['user__first_name', 'user__last_name']





#job search list
class JobSearchListView(generics.ListAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['location', 'job_type', 'industry']
    search_fields = ['title', 'description', 'industry']




class lpOrderRequestView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data.copy()
        data['employer'] = request.user.id

        serializer = OrderRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





from rest_framework import generics, permissions, serializers
from rest_framework.authentication import TokenAuthentication


class OrderRequestCreateView(generics.CreateAPIView):
    queryset = OrderRequest.objects.all()
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



from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import OrderRequest
from .serializers import OrderRequestSerializer

class pkOrderRequestCreateView(generics.CreateAPIView):
    queryset = OrderRequest.objects.all()
    serializer_class = OrderRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer): 
        artisan_id = self.request.data.get('artisan')
        service_id = self.request.data.get('service')

        try:
            artisan = Artisan.objects.get(pk=artisan_id)
            service = Service.objects.get(pk=service_id)
        except (Artisan.DoesNotExist, Service.DoesNotExist):
            raise serializers.ValidationError("Invalid Artisan or Service")

        # Use the authenticated user
        serializer.save(
            artisan=artisan,
            service=service,
            employer=self.request.user.employer
        )


from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import OrderRequest, Artisan, Service
from .serializers import OrderRequestSerializer
from rest_framework import serializers

class klOrderRequestCreateView(generics.CreateAPIView):
    queryset = OrderRequest.objects.all()
    serializer_class = OrderRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        artisan_id = self.request.data.get('artisan')
        service_id = self.request.data.get('service')

        try:
            artisan = Artisan.objects.get(pk=artisan_id)
            service = Service.objects.get(pk=service_id)
        except (Artisan.DoesNotExist, Service.DoesNotExist):
            raise serializers.ValidationError("Invalid Artisan or Service")

        # Ensure the authenticated user is recognized as the employer
        employer = self.request.user.employer  # Assuming there is a one-to-one relationship

        # Save the order request with the provided artisan and service, associated with the authenticated employer
        serializer.save(
            artisan=artisan,
            service=service,
            employer=employer
        )



from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import OrderRequest
from .serializers import OrderRequestSerializer
from rest_framework.permissions import IsAuthenticated

class OnnrderRequestCreateView(generics.CreateAPIView):
    serializer_class = OrderRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        artisan_id = self.request.data.get('artisan')
        service_id = self.request.data.get('service')
        

        try:
            artisan = Artisan.objects.get(pk=artisan_id)
            service = Service.objects.get(pk=service_id)
        except (Artisan.DoesNotExist, Service.DoesNotExist):
            return Response({"detail": "Invalid Artisan or Service"}, status=status.HTTP_400_BAD_REQUEST)

        employer = self.request.user.employer

        serializer.save(
            artisan=artisan,
            service=service,
            employer=employer
        )



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import OrderRequest
from .serializers import OrderRequestSerializer
from django.contrib.auth import get_user_model

@api_view(['POST'])
def order_request(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = OrderRequestSerializer(data=request.data)
    if serializer.is_valid():
        # Add the employer and artisan from the request or from the token
        user = request.user
        employer = user.employer  # Assuming User model has a one-to-one relation with Employer
        artisan_id = request.data.get('artisan_id')
        service_id = request.data.get('service_id')

        # Set the employer and artisan in the validated data
        serializer.validated_data['employer'] = employer
        serializer.validated_data['artisan_id'] = artisan_id
        serializer.validated_data['service_id'] = service_id
        serializer.validated_data['date_ordered'] = timezone.now()

        # Save the order request
        serializer.save()
        return Response({'message': 'Order placed successfully'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import OrderRequest
from .serializers import OrderRequestSerializer

class OrderRequestViewPage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Artisan, Order
from .serializers import OrderRequestSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    user = request.user
    artisan_id = request.data.get('artisan')
    try:
        artisan = Artisan.objects.get(id=artisan_id)
    except Artisan.DoesNotExist:
        return Response({"error": "Artisan not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = OrderRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(employer=user, artisan=artisan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework.views import APIView
from rest_framework.response import Response
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



from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class OrderRequestCreateView(generics.CreateAPIView):
    queryset = OrderRequest.objects.all()
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
