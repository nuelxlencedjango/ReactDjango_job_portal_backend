from django.shortcuts import render

# Create your views here.
# users/views.py
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, ArtisanProfile, EmployerProfile, ManagerProfile
from .serializers import CustomUserSerializer,ArtisanProfileSerializer, EmployerProfileSerializer
from django.core.files.storage import default_storage
from django.conf import settings






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






class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user_serializer = CustomUserSerializer(data=request.data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                return Response({
                    'detail': 'Registration successful!', 'id': user.id, 
                    'username': user.username }, status=status.HTTP_201_CREATED)
            else:
                formatted_errors = {key: value[0] for key, value in user_serializer.errors.items()}
                return Response(formatted_errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class pooArtisanRegistrationDetailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Extract artisan data
            user_info = request.user.id
            artisan_data = request.data

            # Retrieve the user by ID (user should already exist at this point)
            user_id = artisan_data.get('user')
            if not user_id:
                return Response({'error': 'User information is required.','user_info':user_info}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Ensure the user_type is set to 'artisan'
            user.user_type = 'artisan'
            user.save()

            # Add the user instance to the artisan profile data
            artisan_data['user'] = user.id

            # Validate and save the artisan profile
            artisan_serializer = ArtisanProfileSerializer(data=artisan_data)
            if artisan_serializer.is_valid():
                artisan_serializer.save()
                return Response({'detail': 'Artisan profile created successfully!'}, status=status.HTTP_201_CREATED)

            # If validation fails, return errors
            return Response(artisan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










# views.py

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from .models import CustomUser, ArtisanProfile, EmployerProfile, ManagerProfile

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
                "last_name": user.last_name, 'password':user.password, 'user_type':user.user_type  }, status=status.HTTP_201_CREATED)
            else:
                formatted_errors = {key: value[0] for key, value in user_serializer.errors.items()}
                return Response(formatted_errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
       

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import CustomUser, ArtisanProfile, EmployerProfile
from .serializers import ArtisanProfileSerializer, EmployerProfileSerializer

class poUserRegistrationDetailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Ensure the user exists
            user_id = request.data.get('username') 
            #user_type = request.data.get('user_type') 

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
                    artisan_data['user'] = user.id  # Assign the user instance to the artisan profile
                   # artisan_data['user_type'] = "artisan"

                    if 'profile_img' in request.FILES:
                        artisan_data['profile_image'] = request.FILES['profile_img']
                    if 'fingerprint_img' in request.FILES:
                        artisan_data['fingerprint_image'] = request.FILES['fingerprint_img']

                    artisan_serializer = ArtisanProfileSerializer(data=artisan_data)
                    if artisan_serializer.is_valid():
                        artisan_serializer.save()  # Save the new artisan profile
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
                    employer_data['user'] = user.id  # Assign the user instance to the employer profile
                    #employer_data['user_type'] = "employer"

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







from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import CustomUser, ArtisanProfile, EmployerProfile
from .serializers import ArtisanProfileSerializer, EmployerProfileSerializer

class AlortisanRegistrationDetailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Ensure the user exists
            user_id = request.data.get('username')  # 'username' or 'user_id' depending on how it's sent
            user_type = request.data.get('user_type')

            if not user_id:
                return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the user instance (custom user model)
            try:
                user = CustomUser.objects.get(username=user_id)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Process based on user_type (either 'artisan' or 'employer')
            if user_type == "artisan":
                # Ensure the artisan profile doesn't already exist
                artisan_profile = ArtisanProfile.objects.filter(user=user).first()

                # If no artisan profile exists, create a new one
                if not artisan_profile:
                    artisan_data = request.data.copy()  # Make a copy of the data to avoid mutating the original request.data
                    artisan_data['user'] = user.id  # Assign the user ID to the user field

                    # Check if profile_img and fingerprint_img are in the request
                    if 'profile_img' in request.FILES:
                        artisan_data['profile_image'] = request.FILES['profile_img']
                    if 'fingerprint_img' in request.FILES:
                        artisan_data['fingerprint_image'] = request.FILES['fingerprint_img']

                    # Create serializer instance and pass the data
                    artisan_serializer = ArtisanProfileSerializer(data=artisan_data)
                    if artisan_serializer.is_valid():
                        artisan_serializer.save()  # Save the new artisan profile
                        return Response({'detail': 'Artisan profile created successfully!'}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(artisan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Artisan profile already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)

            elif user_type == "employer":
                # Ensure the employer profile doesn't already exist
                employer_profile = EmployerProfile.objects.filter(user=user).first()

                # If no employer profile exists, create a new one
                if not employer_profile:
                    employer_data = request.data.copy()  # Make a copy of the data
                    employer_data['user'] = user.id  # Assign the user ID to the user field

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
            # Handle unexpected errors
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

                    # If profile_img or fingerprint_img are provided, add them
                    if 'profile_img' in request.FILES:
                        artisan_data.profile_image = request.FILES['profile_img']
                    if 'fingerprint_img' in request.FILES:
                        artisan_data.fingerprint_image = request.FILES['fingerprint_img']

                    artisan_serializer = ArtisanProfileSerializer(data=artisan_data)
                    if artisan_serializer.is_valid():
                        artisan_serializer.save()  # Save the new artisan profile
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
