
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from acct.serializers import (CustomUserSerializer, ArtisanProfileSerializer, 
                              EmployerProfileSerializer)
from django.db import transaction
from acct.models import CustomUser,ArtisanProfile,MarketerProfile
from rest_framework.permissions import IsAuthenticated

from .serializers import ArtisanSearchListSerializer


import logging

logger = logging.getLogger(__name__)



class ArtisanRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            with transaction.atomic():
                # Identify marketer
                marketer = None
                if request.user.is_authenticated and request.user.user_type == 'marketer':
                    try:
                        marketer = MarketerProfile.objects.get(user=request.user)
                        logger.info(f"Marketer found via request.user: {marketer.user.username}")
                    except MarketerProfile.DoesNotExist:
                        logger.warning(f"Authenticated user {request.user.username} has no MarketerProfile")
                elif request.data.get('marketer_id'):
                    try:
                        marketer_user = CustomUser.objects.get(id=request.data['marketer_id'], user_type='marketer')
                        marketer = MarketerProfile.objects.get(user=marketer_user)
                        logger.info(f"Marketer found via marketer_id: {marketer.user.username}")
                    except (CustomUser.DoesNotExist, MarketerProfile.DoesNotExist):
                        logger.error(f"Invalid marketer_id: {request.data['marketer_id']}")
                        return Response({'marketer_id': 'Marketer not found.'}, status=status.HTTP_400_BAD_REQUEST)

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
                    return Response({
                        'id': user.id,
                        'username': user.username,
                        'detail': 'Artisan registered successfully.'
                    }, status=status.HTTP_201_CREATED)
                else:
                    logger.error(f"Artisan serializer errors: {artisan_serializer.errors}")
                    return Response(artisan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        




class MarketerArtisansListView(APIView): 
    permission_classes = [IsAuthenticated] 
    
    def get(self, request):
        try:
            
            marketer_profile = request.user.marketer_profile  
            logger.info(f"Marketer found via request.user: {marketer_profile}")
            lst_artisans = ArtisanProfile.objects.filter(marketer=marketer_profile)
            logger.info(f"Marketer artisans: {lst_artisans}")
            serializer = ArtisanSearchListSerializer(lst_artisans, many=True)
            logger.info(f"Marketer serializer: {serializer}")
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except AttributeError:
            
            return Response({"error": "User is not a marketer"}, status=status.HTTP_403_FORBIDDEN)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

