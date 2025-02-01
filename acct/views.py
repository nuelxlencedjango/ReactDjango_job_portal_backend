from django.shortcuts import render

# Create your views here.
# users/views.py
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from .models import CustomUser, ArtisanProfile, EmployerProfile,Fingerprint
from .serializers import CustomUserSerializer,ArtisanProfileSerializer, EmployerProfileSerializer
from django.core.files.storage import default_storage
from django.conf import settings

import base64
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

#from django.contrib.auth import get_user_model


#User = get_user_model() 


# views.py

class UserRegistrationAndProfileCreation(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            user_serializer = CustomUserSerializer(data=request.data)
        
            if user_serializer.is_valid():
                user = user_serializer.save()  # Create the user
            
                # Trigger profile creation via signals (handled by Django signals)
         
                return Response({ "id": user.id,"username": user.username,
                "email": user.email,"first_name": user.first_name,
                "last_name": user.last_name, 'user_type':user.user_type  }, status=status.HTTP_201_CREATED)
            else:
                formatted_errors = {key: value[0] for key, value in user_serializer.errors.items()}
                return Response(formatted_errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
       






class UserRegistrationDetailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Ensure the user exists
            user_id = request.data.get('username')  # Use 'username' as the identifier
            if not user_id:
                return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the user instance
            try:
                user = CustomUser.objects.get(username=user_id)
                
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Process based on user_type (either 'artisan' or 'employer')
            if user.user_type == "artisan":
                # Ensure the artisan profile doesn't already exist
                artisan_profile = ArtisanProfile.objects.filter(user=user).first()

                # If no artisan profile exists, create a new one
                if not artisan_profile:
                    artisan_data = request.data.copy()  # Make a copy of the data
                    artisan_data['user'] = user.id  # Assign the user ID to the artisan profile

                    artisan_serializer = ArtisanProfileSerializer(data=artisan_data)
                    if artisan_serializer.is_valid():
                        artisan = artisan_serializer.save() 
                        if 'profile_image' in request.FILES:
                            artisan.profile_image = request.FILES['profile_image']
                        artisan.save()    
                         # Save the new artisan profile
                        return Response({'detail': 'Artisan profile created successfully!'}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(artisan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Artisan profile already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)

            elif user.user_type == "employer":
                # Ensure the employer profile doesn't already exist
                employer_profile = EmployerProfile.objects.filter(user=user).first()

                # If no employer profile exists, create a new one
                if not employer_profile:
                    employer_data = request.data.copy()  # Make a copy of the data
                    employer_data['user'] = user.id  # Assign the user ID to the employer profile

                    employer_serializer = EmployerProfileSerializer(data=employer_data)
                    if employer_serializer.is_valid():
                        employer_serializer.save()  # Save the new employer profile
                        return Response({'detail': 'Employer profile created successfully!'}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(employer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Employer profile already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'error': 'Invalid user type.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handle any unexpected errors
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





def set_cookie(response, token, cookie_name):
    response.set_cookie(cookie_name,token,httponly=True,secure=True,samesite='Lax',
        path='/',)
    

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

        response = Response({'refresh': refresh_token,'access': access_token,'user_type': user.user_type,})

        set_cookie(response, access_token, 'access_token')
        set_cookie(response, refresh_token, 'refresh_token')

        return response





class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the refresh token from request
            refresh_token = request.data.get('refresh_token')
            
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token to prevent further use
            return Response({"message": "Logged out successfully"}, status=200)

        except Exception as e:
            return Response({"message": str(e)}, status=400)



# views.py



from .models import Fingerprint, ArtisanProfile
from .serializers import FingerprintSerializer
from django.core.files.base import ContentFile
import base64

class FingerprintUploadViewlpld(APIView):
    def post(self, request, *args, **kwargs):
        # Ensure user is authenticated and get the artisan profile
        artisan_profile = ArtisanProfile.objects.get(user=request.user)
        if not artisan_profile:
            return Response({'error': 'User Profile not found.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the fingerprint image
        fingerprint_image = request.FILES.get('fingerprint_image') or request.data.get('fingerprint_image')
        
        if not fingerprint_image:
            return Response({'error': 'Fingerprint image.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Step 2: If it's a base64 string (optional), decode it
        if isinstance(fingerprint_image, str):  # Check if base64 string
            if fingerprint_image.startswith('data:image'):
                image_data = fingerprint_image.split(",")[1]
                image_data = base64.b64decode(image_data)
                fingerprint_image = ContentFile(image_data, name="fingerprint_image.jpg")
        
        # Step 3: Create a Fingerprint record
        fingerprint = Fingerprint(
            artisan_profile=artisan_profile,
            fingerprint_image=fingerprint_image,
           
        )
        
        fingerprint.save()

        # Step 4: Return success response
        return Response({
            'message': 'Fingerprint uploaded successfully.',
            'fingerprint_id': fingerprint.id
        }, status=status.HTTP_201_CREATED)






class FingerprintUploadView(APIView):
    def post(self, request, *args, **kwargs):
        # Ensure user is authenticated and get the artisan profile
        artisan_profile = ArtisanProfile.objects.get(user=request.user)
        if not artisan_profile:
            return Response({'error': 'User Profile not found.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the fingerprint image from the request (either as a file or base64 string)
        fingerprint_image = request.FILES.get('fingerprint_image') or request.data.get('fingerprint_image')

        if not fingerprint_image:
            return Response({'error': 'Fingerprint image is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Step 1: Validate if it's a valid image file (PNG, JPG, JPEG)
        if isinstance(fingerprint_image, str):  # If it's a base64 string
            if fingerprint_image.startswith('data:image'):
                # Decode base64 string into an image file
                image_data = fingerprint_image.split(",")[1]
                image_data = base64.b64decode(image_data)
                fingerprint_image = ContentFile(image_data, name="fingerprint_image.jpg")  # Temporary file name

        # Step 2: Validate file type for images (only PNG, JPG, JPEG)
        if isinstance(fingerprint_image, ContentFile):  # If it's a file (either uploaded or from base64)
            try:
                image = Image.open(fingerprint_image)
                image_format = image.format.lower()

                if image_format not in ['jpeg', 'png']:
                    raise ValidationError("Invalid image format. Only PNG, JPG, or JPEG are allowed.")
            except Exception as e:
                return Response({'error': 'Invalid image file.'}, status=status.HTTP_400_BAD_REQUEST)

        # Step 3: Create a Fingerprint record
        fingerprint = Fingerprint(
            artisan_profile=artisan_profile,
            fingerprint_image=fingerprint_image,
        )

        fingerprint.save()

        # Step 4: Return success response
        return Response({
            'message': 'Fingerprint uploaded successfully.',
            'fingerprint_id': fingerprint.id
        }, status=status.HTTP_201_CREATED)
