from django.shortcuts import render
from rest_framework import generics, status,serializers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from rest_framework.response import Response

from rest_framework.views import APIView

from accounts.serializers import *
from artisans.models import *
from django.conf import settings
#from .models import User
import json






class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({"message": "Logout successful"})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response







# views.py

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

User = get_user_model()

def set_cookie(response, token, cookie_name):
    response.set_cookie(
        cookie_name,
        token,
        httponly=True,
        secure=True,
        samesite='Lax',
        path='/',
    )

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({
            'refresh': refresh_token,
            'access': access_token,
        })
        set_cookie(response, access_token, 'access_token')
        set_cookie(response, refresh_token, 'refresh_token')

        return response


'''


# views.py
class assArtisanUserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            headers = self.get_success_headers(serializer.data)
            
            # Include the user ID in the response
            response_data = {
                
                'id': serializer.instance.id, 
                'username': serializer.instance.username, 
                **serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        
        except serializers.ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        except json.JSONDecodeError as e:
            return Response({"error": "Invalid JSON data: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


'''






# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer

class ArtisanRegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Artisan registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployerRegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Employer registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ManagerRegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Manager registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
