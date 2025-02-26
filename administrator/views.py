from django.shortcuts import render

# Create your views here.


# views.py
from django.http import JsonResponse
from django.views import View
from acct.models import ArtisanProfile
from .serializers import ArtisanProfileSerializer, CompanySerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Company





class ArtisanSearchView(View):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get query parameters
        name = request.GET.get('name', '')
        email = request.GET.get('email', '')
        phone_number = request.GET.get('phone_number', '')

        # Filter artisans based on the provided parameters
        artisans = ArtisanProfile.objects.all()
        if name:
            artisans = artisans.filter(user__first_name__icontains=name)
        if email:
            artisans = artisans.filter(user__email__icontains=email)
        if phone_number:
            artisans = artisans.filter(phone_number__icontains=phone_number)

        # Serialize the results
        results = [
            {
                'id': artisan.id,
                'name': artisan.user.first_name,
                'email': artisan.user.email,
                'phone_number': artisan.phone_number,
                'service': artisan.service.title if artisan.service else None,
                'experience': artisan.experience,
                'location': artisan.location.location if artisan.location else None,
                'profile_image': artisan.profile_image.url if artisan.profile_image else None,
            }
            for artisan in artisans
        ]

        return JsonResponse(results, safe=False)

    

class CompanyListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)

        # Return the companies as an object with a 'companies' key
        return Response({
            'companies': serializer.data  
        })
