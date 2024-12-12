from django.shortcuts import render

# Create your views here.
# users/views.py
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, ArtisanProfile, EmployerProfile, ManagerProfile
from .serializers import CustomUserSerializer
from django.core.files.storage import default_storage
from django.conf import settings

class xzArtisanRegistrationView(APIView):
    def post(self, request):
        data = request.data
        user_data = {
            "username": data["username"],
            "email": data["email"],
            "user_type": "artisan",
        }
        
        # Save user
        user = CustomUser.objects.create_user(**user_data, password=data["password"])
        
        # Create Artisan Profile
        ArtisanProfile.objects.create(
            user=user,
            experience=data["experience"],
            job_type=data["job_type"],
            profile_image=data.get("profile_image", None),
            fingerprint_image=data.get("fingerprint_image", None),
            industry=data.get("industry", None),
            pay=data.get("pay", None),
            nin=data["nin"]
        )
        
        return Response({"message": "Artisan registered successfully!"}, status=status.HTTP_201_CREATED)


class polEmployerRegistrationView(APIView):
    def post(self, request):
        data = request.data
        user_data = {
            "username": data["username"],
            "email": data["email"],
            "user_type": "employer",
        }

        # Save user
        user = CustomUser.objects.create_user(**user_data, password=data["password"])
        
        # Create Employer Profile
        EmployerProfile.objects.create(
            user=user,
            company_name=data["company_name"],
            company_address=data["company_address"]
        )
        
        return Response({"message": "Employer registered successfully!"}, status=status.HTTP_201_CREATED)


class llManagerRegistrationView(APIView):
    def post(self, request):
        data = request.data
        user_data = {
            "username": data["username"],
            "email": data["email"],
            "user_type": "manager",
        }

        # Save user
        user = CustomUser.objects.create_user(**user_data, password=data["password"])
        
        # Create Manager Profile
        ManagerProfile.objects.create(
            user=user,
            department=data["department"]
        )
        
        return Response({"message": "Manager registered successfully!"}, status=status.HTTP_201_CREATED)









from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, ArtisanProfile, EmployerProfile
from .serializers import CustomUserSerializer, ArtisanProfileSerializer, EmployerProfileSerializer

class mkArtisanRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user_serializer = CustomUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            artisan_profile_data = request.data.copy()  # Copy request data
            artisan_profile_data['user'] = user.id
            artisan_serializer = ArtisanProfileSerializer(data=artisan_profile_data)
            if artisan_serializer.is_valid():
                artisan_serializer.save()
                return Response({'detail': 'Registration successful!'}, status=status.HTTP_201_CREATED)
            return Response(artisan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ytEmployerRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user_serializer = CustomUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            employer_profile_data = request.data.copy()
            employer_profile_data['user'] = user.id
            employer_serializer = EmployerProfileSerializer(data=employer_profile_data)
            if employer_serializer.is_valid():
                employer_serializer.save()
                return Response({'detail': 'Registration successful!'}, status=status.HTTP_201_CREATED)
            return Response(employer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)








from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import CustomUserSerializer, ArtisanProfileSerializer, EmployerProfileSerializer
from .models import CustomUser, ArtisanProfile, EmployerProfile

class bvApprtisanRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_serializer = CustomUserSerializer(data=request.data)
        
        if user_serializer.is_valid():
            # Save the user
            user = user_serializer.save()
            
            # Copy the data for ArtisanProfile and add the user ID
            artisan_profile_data = request.data.copy()
            artisan_profile_data['user'] = user.id
            
            # Serialize and save ArtisanProfile
            artisan_serializer = ArtisanProfileSerializer(data=artisan_profile_data)
            if artisan_serializer.is_valid():
                artisan_serializer.save()
                return Response({'detail': 'Registration successful!'}, status=status.HTTP_201_CREATED)
            return Response(artisan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class kEmployerRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_serializer = CustomUserSerializer(data=request.data)
        
        if user_serializer.is_valid():
            # Save the user
            user = user_serializer.save()
            
            # Copy the data for EmployerProfile and add the user ID
            employer_profile_data = request.data.copy()
            employer_profile_data['user'] = user.id
            
            # Serialize and save EmployerProfile
            employer_serializer = EmployerProfileSerializer(data=employer_profile_data)
            if employer_serializer.is_valid():
                employer_serializer.save()
                return Response({'detail': 'Registration successful!'}, status=status.HTTP_201_CREATED)
            return Response(employer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)





from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import CustomUser, ArtisanProfile, EmployerProfile
from .serializers import CustomUserSerializer, ArtisanProfileSerializer, EmployerProfileSerializer

class mnArtisanRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Start a transaction block
        with transaction.atomic():
            user_serializer = CustomUserSerializer(data=request.data)
            if user_serializer.is_valid():
                # Create the user
                user = user_serializer.save()
                
                # Now, try creating the artisan profile
                artisan_profile_data = request.data.copy()  # Copy request data
                artisan_profile_data['user'] = user.id
                artisan_serializer = ArtisanProfileSerializer(data=artisan_profile_data)
                
                if artisan_serializer.is_valid():
                    artisan_serializer.save()
                    return Response({'detail': 'Registration successful!'}, status=status.HTTP_201_CREATED)
                else:
                    # If ArtisanProfile creation fails, raise an exception to roll back the transaction
                    raise Exception("Artisan profile creation failed!")
            else:
                # If user creation fails, raise an exception to roll back the transaction
                raise Exception("User creation failed!")
        # If anything goes wrong, the transaction will automatically roll back
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class vcEmployerRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Start a transaction block
        with transaction.atomic():
            user_serializer = CustomUserSerializer(data=request.data)
            if user_serializer.is_valid():
                # Create the user
                user = user_serializer.save()

                # Now, try creating the employer profile
                employer_profile_data = request.data.copy()  # Copy request data
                employer_profile_data['user'] = user.id
                employer_serializer = EmployerProfileSerializer(data=employer_profile_data)
                
                if employer_serializer.is_valid():
                    employer_serializer.save()
                    return Response({'detail': 'Registration successful!'}, status=status.HTTP_201_CREATED)
                else:
                    # If EmployerProfile creation fails, raise an exception to roll back the transaction
                    raise Exception("Employer profile creation failed!")
            else:
                # If user creation fails, raise an exception to roll back the transaction
                raise Exception("User creation failed!")
        # If anything goes wrong, the transaction will automatically roll back
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)








# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db import transaction
from .serializers import CustomUserSerializer, ArtisanProfileSerializer, EmployerProfileSerializer
from .models import CustomUser


class ltArtisanRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Start a transaction block
        with transaction.atomic():
            user_serializer = CustomUserSerializer(data=request.data)
            if user_serializer.is_valid():
                # Create the user
                user = user_serializer.save()

                # Now, try creating the artisan profile
                artisan_profile_data = request.data.copy()
                artisan_profile_data['user'] = user.id
                artisan_serializer = ArtisanProfileSerializer(data=artisan_profile_data)
                
                if artisan_serializer.is_valid():
                    artisan_serializer.save()
                    return Response({'detail': 'Registration successful!'}, status=status.HTTP_201_CREATED)
                else:
                    # If ArtisanProfile creation fails, return the errors
                    return Response(artisan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If user creation fails, return the errors
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class kkEmployerRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Start a transaction block
        with transaction.atomic():
            user_serializer = CustomUserSerializer(data=request.data)
            if user_serializer.is_valid():
                # Create the user
                user = user_serializer.save()

                # Now, try creating the employer profile
                employer_profile_data = request.data.copy()
                employer_profile_data['user'] = user.id
                employer_serializer = EmployerProfileSerializer(data=employer_profile_data)
                
                if employer_serializer.is_valid():
                    employer_serializer.save()
                    return Response({'detail': 'Registration successful!'}, status=status.HTTP_201_CREATED)
                else:
                    # If EmployerProfile creation fails, return the errors
                    return Response(employer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If user creation fails, return the errors
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)





from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from .models import *
from .serializers import *

@api_view(['POST'])
def artisan_or_employer_register(request):
    csrf_token = request.META.get('HTTP_X_CSRFTOKEN')

    # Validate CSRF token
    if not csrf_token or not validate_csrf_token(csrf_token):
        return JsonResponse({"error": "Invalid CSRF token"}, status=403)

    user_type = request.data.get('user_type')

    if user_type == "artisan":
        serializer = ArtisanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif user_type == "employer":
        serializer = EmployerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    return JsonResponse({"error": "Invalid user type"}, status=400)





from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import CustomUserSerializer

class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            user_serializer = CustomUserSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({'detail': 'Registration successful!'}, status=status.HTTP_201_CREATED)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


