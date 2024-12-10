from django.shortcuts import render

# Create your views here.
# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, ArtisanProfile, EmployerProfile, ManagerProfile
from .serializers import CustomUserSerializer
from django.core.files.storage import default_storage
from django.conf import settings

class ArtisanRegistrationView(APIView):
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


class EmployerRegistrationView(APIView):
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


class ManagerRegistrationView(APIView):
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
