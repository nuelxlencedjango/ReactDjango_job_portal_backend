
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from acct.models import  MarketerProfile
from acct.serializers import CustomUserSerializer, ArtisanProfileSerializer, EmployerProfileSerializer
from django.db import transaction

import logging

logger = logging.getLogger(__name__)


class MarketerRegistrationView101(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # check the marketer exists
            marketer_id = request.user
            if not marketer_id:
                return Response({'error': 'Marketer ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                marketer = MarketerProfile.objects.get(user=marketer_id)
            except MarketerProfile.DoesNotExist:
                return Response({'error': 'Marketer not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Create the user
            user_serializer = CustomUserSerializer(data=request.data)
            if user_serializer.is_valid():
                user = user_serializer.save()

                # Create the profile based on user type
                if user.user_type == "artisan":
                    artisan_data = request.data.copy()
                    artisan_data['user'] = user.id
                    artisan_data['marketer'] = marketer.id

                    artisan_serializer = ArtisanProfileSerializer(data=artisan_data)
                    if artisan_serializer.is_valid():
                        artisan_serializer.save()
                        return Response({'detail': 'Artisan registered successfully by marketer.'}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(artisan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                elif user.user_type == "employer":
                    employer_data = request.data.copy()
                    employer_data['user'] = user.id
                    employer_data['marketer'] = marketer.id

                    employer_serializer = EmployerProfileSerializer(data=employer_data)
                    if employer_serializer.is_valid():
                        employer_serializer.save()
                        return Response({'detail': 'Employer registered successfully by marketer.'}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(employer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'error': 'Invalid user type.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        




class ArtisanRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            if MarketerProfile.objects.get(username = request.user):

                marketer = MarketerProfile.objects.get(username= request.user)
                logger.info(f"Marketer found: {marketer.user.username}")

                return Response({'marketer_code': 'Marketer profile not found.'}, 
                                status=status.HTTP_400_BAD_REQUEST)


            with transaction.atomic():
                # Validate and create CustomUser
                user_data = {
                    'username': request.data.get('username'),
                    'first_name': request.data.get('first_name'),
                    'last_name': request.data.get('last_name'),
                    'email': request.data.get('email'),
                    'password': request.data.get('password'),
                    'password2': request.data.get('password2'),
                    'user_type': request.data.get('user_type', 'artisan'),
                }
                user_serializer = CustomUserSerializer(data=user_data)
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    logger.info(f"User created: {user.username}")
                else:
                    logger.error(f"User serializer errors: {user_serializer.errors}")
                    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

               
                # Create ArtisanProfile
                artisan_data = request.data.copy()
                artisan_data['user'] = user.id
                if marketer:
                    artisan_data['marketer'] = marketer.id
                artisan_serializer = ArtisanProfileSerializer(data=artisan_data)
                if artisan_serializer.is_valid():
                    artisan_serializer.save()
                    logger.info(f"Artisan profile created for user: {user.username}")
                    return Response({'id': user.id,'username': user.username,
                        'detail': 'Artisan registered successfully.'}, 
                        status=status.HTTP_201_CREATED)
                else:
                    logger.error(f"Artisan serializer errors: {artisan_serializer.errors}")
                    return Response(artisan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
