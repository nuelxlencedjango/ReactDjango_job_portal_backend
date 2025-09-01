
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from .models import CustomUser, ArtisanProfile, EmployerProfile,Fingerprint
from .serializers import (CustomUserSerializer,ArtisanProfileSerializer, UserProfileSerializer, 
                          EmployerProfileSerializer,FingerprintSerializer)
from django.core.files.storage import default_storage
from django.conf import settings

import base64
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from PIL import Image
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User





from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()




import logging

logger = logging.getLogger(__name__)

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
                "last_name": user.last_name, 'user_type':user.user_type  }, 
                status=status.HTTP_201_CREATED)
            else:
                formatted_errors = {key: value[0] for key, value in user_serializer.errors.items()}
                return Response(formatted_errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class UserRegistrationDetailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user_id = request.data.get('username')
            if not user_id:
                logger.error("Username is required.")
                return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = CustomUser.objects.get(username=user_id)
                logger.info(f"User found: {user.username}")
            except CustomUser.DoesNotExist:
                logger.error(f"User not found: {user_id}")
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

            if user.user_type == "artisan":
                artisan_profile = ArtisanProfile.objects.filter(user=user).first()
                logger.info(f"Artisan profile details: {artisan_profile}")
                
                if not artisan_profile:
                    artisan_data = request.data.copy()
                    artisan_data['user'] = user.id
                    logger.info(f"Artisan user info: {artisan_data}")

                    artisan_serializer = ArtisanProfileSerializer(data=artisan_data)
                    logger.info(f"Artisan serializer info: {artisan_serializer}")
                    if artisan_serializer.is_valid():
                        artisan = artisan_serializer.save()
                        logger.info(f"Artisan serializer saved: {artisan}")
                        return Response({'detail': 'Artisan profile created successfully!'}, status=status.HTTP_201_CREATED)
                    else:
                        logger.error(f"Artisan serializer errors: {artisan_serializer.errors}")
                        return Response(artisan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    logger.error("Artisan profile already exists for this user.")
                    return Response({'error': 'Artisan profile already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)

            elif user.user_type == "employer":
                employer_profile = EmployerProfile.objects.filter(user=user).first()
                if not employer_profile:
                    employer_data = request.data.copy()
                    employer_data['user'] = user.id
                    employer_serializer = EmployerProfileSerializer(data=employer_data)
                    if employer_serializer.is_valid():
                        employer_serializer.save()
                        logger.info("Employer profile created successfully.")
                        return Response({'detail': 'Employer profile created successfully!'}, status=status.HTTP_201_CREATED)
                    else:
                        logger.error(f"Employer serializer errors: {employer_serializer.errors}")
                        return Response(employer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    logger.error("Employer profile already exists for this user.")
                    return Response({'error': 'Employer profile already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                logger.error(f"Invalid user type: {user.user_type}")
                return Response({'error': 'Invalid user type.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
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

        response = Response({'refresh': refresh_token,'access': access_token,
                             'user_type': user.user_type,})

        set_cookie(response, access_token, 'access_token')
        set_cookie(response, refresh_token, 'refresh_token')

        return response
    


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=400)
                
            token = RefreshToken(refresh_token)
            token.blacklist()  # Invalidate the refresh token
            
            #  access token to blacklist
            try:
                access_token = request.auth.token
                RefreshToken(access_token).blacklist()
            except Exception:
                pass  
                
            return Response({"message": "Successfully logged out"}, status=200)
            
        except Exception as e:
            return Response({"error": str(e)}, status=400)




#Getting user details
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)





class FingerprintUploadView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request, artisan_id, *args, **kwargs):
        try:
            # artisan profile by ID
            artisan_profile = ArtisanProfile.objects.get(id=artisan_id)
        except ArtisanProfile.DoesNotExist:
            return Response({'error': 'Artisan profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        # the fingerprint image from the request (either as a file or base64 string)
        fingerprint_image = request.FILES.get('fingerprint_image') or request.data.get('fingerprint_image')

        if not fingerprint_image:
            return Response({'error': 'Fingerprint image is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate if it's a valid image file (PNG, JPG, JPEG)
        if isinstance(fingerprint_image, str):  # If it's a base64 string
            if fingerprint_image.startswith('data:image'):
                # Decode base64 string into an image file
                image_data = fingerprint_image.split(",")[1]
                image_data = base64.b64decode(image_data)
                fingerprint_image = ContentFile(image_data, name="fingerprint_image.jpg")

        # File type for images (only PNG, JPG, JPEG)
        if isinstance(fingerprint_image, ContentFile):
            try:
                image = Image.open(fingerprint_image)
                image_format = image.format.lower()

                if image_format not in ['jpeg', 'png']:
                    return Response({'error': 'Invalid image format. Only PNG, JPG, or JPEG are allowed.'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': 'Invalid image file.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a Fingerprint record
        fingerprint = Fingerprint(
            artisan_profile=artisan_profile, fingerprint_image=fingerprint_image,)
        fingerprint.save()

        # Return success response
        return Response({'message': 'Fingerprint uploaded successfully.',
            'fingerprint_id': fingerprint.id }, status=status.HTTP_201_CREATED)







from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings




class PasswordResetRequestView9000(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        logger.info(f"email recieved: {email}")
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
            logger.info(f"user with email seen: {user}")
        except CustomUser.DoesNotExist:
            return Response({'error': 'No user with this email exists'}, status=status.HTTP_404_NOT_FOUND)
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        logger.info(f"user token: {token}")
        logger.info(f"uid: {uid}")
        logger.info(f"frontend url: {reset_url}")

        
        subject = "Password Reset Request"
        message = f"""
        Hello {user.username},
        
        You requested a password reset. Please click the link below to reset your password:
        
        {reset_url}
        
        If you didn't request this, please ignore this email.
        
        Thanks,
        I-wan-wok.com
        """
        logger.info(f"user details: {subject}")
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
            logger.info(f"message sent: {send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)}")
            return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error({e})
            return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)

class PasswordResetRequestView1111(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        logger.info(f"Received email: {email}")
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
            logger.info(f"Found user: {user.email}")
        except CustomUser.DoesNotExist:
            return Response({'error': 'No user with this email exists'}, status=status.HTTP_404_NOT_FOUND)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        logger.info(f"Generated token: {token}")
        logger.info(f"Generated uid: {uid}")
        logger.info(f"Reset URL: {reset_url}")

        subject = "Password Reset Request"
        message = f"""Hello {user.username},\n\nYou requested a password reset. Click: {reset_url}\n\nIf not you, ignore.\n\nThanks,\nI-wan-wok.com"""
        logger.info(f"Sending email with subject: {subject}")
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
            logger.info("Email sent successfully")
            return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Email send failed: {str(e)}")
            return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)
    





import threading
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

def send_email_async(subject, message, from_email, recipient_list, html_message=None):
    """Send email in background thread"""
    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
            html_message=html_message
        )
        logger.info("Email sent successfully via async thread")
    except Exception as e:
        logger.error(f"Async email failed: {e}")
        

class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        logger.info(f"email received: {email}")
        
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
            logger.info(f"user with email found: {user}")
        except CustomUser.DoesNotExist:
            return Response({'error': 'No user with this email exists'}, status=status.HTTP_404_NOT_FOUND)
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        
        subject = "Password Reset Request"
        message = f"""Hello {user.username},
        
You requested a password reset. Please click the link below to reset your password:

{reset_url}

If you didn't request this, please ignore this email.

Thanks,
I-wan-wok.com"""
        
        # HTML version
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <body>
            <p>Hello {user.username},</p>
            <p>You requested a password reset. Please click the link below to reset your password:</p>
            <p><a href="{reset_url}">Reset Password</a></p>
            <p>If you didn't request this, please ignore this email.</p>
            <p>Thanks,<br>I-wan-wok.com Team</p>
        </body>
        </html>
        """
        
        # Send email in background thread
        try:
            email_thread = threading.Thread(
                target=send_email_async,
                args=(subject, message, settings.DEFAULT_FROM_EMAIL, [email]),
                kwargs={'html_message': html_message}
            )
            email_thread.daemon = True
            email_thread.start()
            
            logger.info("Password reset email queued for async sending")
            return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Failed to start email thread: {e}")
            return Response({'error': 'Failed to send email. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)