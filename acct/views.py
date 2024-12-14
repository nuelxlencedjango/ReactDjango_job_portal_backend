from django.shortcuts import render

# Create your views here.
# users/views.py
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, ArtisanProfile, EmployerProfile
from .serializers import CustomUserSerializer,ArtisanProfileSerializer, EmployerProfileSerializer
from django.core.files.storage import default_storage
from django.conf import settings





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
                "last_name": user.last_name, 'password':user.password, 'user_type':user.user_type  }, status=status.HTTP_201_CREATED)
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
