from django.shortcuts import render
from rest_framework import generics, status,serializers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from accounts.serializers import *
from artisans.models import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
import json





class LoginView(generics.GenericAPIView):
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




#create /add profess
class ArtisanUserCreateView(generics.CreateAPIView):
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
