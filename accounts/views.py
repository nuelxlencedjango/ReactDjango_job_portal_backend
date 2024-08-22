from django.shortcuts import render
from rest_framework import generics, status,serializers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

#from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView



from accounts.serializers import *
from artisans.models import *
from django.conf import settings
from .models import User
import json





class eeLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user": UserSerializer(user, context=self.get_serializer_context()).data
        })



class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({"message": "Logout successful"})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response




class mkLoginView(APIView):
    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = Response()

            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=str(refresh.access_token),
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=True,
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            response.data = {"message": "Login successful"}
            return response
        return Response({"error": "Invalid credentials"}, status=400)



class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        tokens = response.data
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=tokens['access'],
            httponly=True,
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN']
        )
        response.set_cookie(
            key='refresh_token',
            value=tokens['refresh'],
            httponly=True,
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
            path=settings.SIMPLE_JWT['REFRESH_COOKIE_PATH'],
        )
        return response


#create /add profess
class tyArtisanUserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]



# views.py
class ArtisanUserCreateView(generics.CreateAPIView):
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
