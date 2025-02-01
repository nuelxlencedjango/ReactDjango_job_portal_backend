from django.shortcuts import render

# Create your views here.









# views.py
from django.http import JsonResponse
from django.views import View
from acct.models import ArtisanProfile
from .serializers import ArtisanProfileSerializer

class ArtisanSearchView(View):
    def get(self, request, *args, **kwargs):
        # Get query parameters
        name = request.GET.get('name', '')
        email = request.GET.get('email', '')
        phone_number = request.GET.get('phone_number', '')

        # Filter artisans based on the provided parameters
        artisans = ArtisanProfile.objects.all()
        if name:
            artisans = artisans.filter(user__username__icontains=name)
        if email:
            artisans = artisans.filter(user__email__icontains=email)
        if phone_number:
            artisans = artisans.filter(phone_number__icontains=phone_number)

        # Serialize the results
        serializer = ArtisanProfileSerializer(artisans, many=True)
        return JsonResponse(serializer.data, safe=False)



from django.http import JsonResponse
from django.views import View


class ArtisanSearchView2(View):
    def get(self, request, *args, **kwargs):
        # Get query parameters
        name = request.GET.get('name', '')
        email = request.GET.get('email', '')
        phone_number = request.GET.get('phone_number', '')

        # Filter artisans based on the provided parameters
        artisans = ArtisanProfile.objects.all()
        if name:
            artisans = artisans.filter(user__username__icontains=name)
        if email:
            artisans = artisans.filter(user__email__icontains=email)
        if phone_number:
            artisans = artisans.filter(phone_number__icontains=phone_number)

        # Serialize the results
        results = [
            {
                'id': artisan.id,
                'name': artisan.user.username,
                'email': artisan.user.email,
                'phone_number': artisan.phone_number,
                'service': artisan.service.title if artisan.service else None,
                'experience': artisan.experience,
                'location': artisan.location.name if artisan.location else None,
                'profile_image': artisan.profile_image.url if artisan.profile_image else None,
            }
            for artisan in artisans
        ]

        return JsonResponse(results, safe=False)




# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .serializers import ArtisanProfileSerializer

class ArtisanProfileViewSet(viewsets.ModelViewSet):
    queryset = ArtisanProfile.objects.all()
    serializer_class = ArtisanProfileSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('query', '')
        artisans = ArtisanProfile.objects.filter(
            Q(user__username__icontains=query) |  # search by username (name)
            Q(user__email__icontains=query) |  # search by email
            Q(phone_number__icontains=query)  # search by phone number
        )
        serializer = self.get_serializer(artisans, many=True)
        return Response(serializer.data)



# artisan_search_view.py
from django.shortcuts import render
from django.http import JsonResponse

from django.views import View

class ArtisanSearchView2(View):
    def get(self, request):
        query = request.GET.get('query', '')
        artisans = ArtisanProfile.objects.filter(
            Q(user__username__icontains=query) | 
            Q(user__email__icontains=query) | 
            Q(phone_number__icontains=query)
        )
        artisan_data = [{"name": artisan.user.username, "email": artisan.user.email} for artisan in artisans]
        return JsonResponse(artisan_data, safe=False)
