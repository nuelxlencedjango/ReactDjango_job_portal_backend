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

class ArtisanRegistrationView(APIView):
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


class EmployerRegistrationView(APIView):
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
