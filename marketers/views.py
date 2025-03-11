
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from acct.models import  MarketerProfile
from acct.serializers import CustomUserSerializer, ArtisanProfileSerializer, EmployerProfileSerializer



class MarketerRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # check the marketer exists
            marketer_id = request.data.get('username')
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