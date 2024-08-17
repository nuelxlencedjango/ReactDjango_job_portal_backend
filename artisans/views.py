from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

import logging 
import json

from artisans.models import *
from artisans.serializers import *
from accounts.serializers import *
from django.db import transaction


logger = logging.getLogger(__name__) 



#list Area objects
class AreaListView(generics.ListAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [AllowAny]


#create/add location/areas
class AreaCreateView(generics.CreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [AllowAny]




#list Profession objects
class ProfessionListView(generics.ListAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    permission_classes = [AllowAny]

#list Profession objects
class ServiceListView(generics.ListAPIView):  
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]




#create /add profess
class ProfessionCreateView(generics.CreateAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    permission_classes = [AllowAny]



#list Artisans objects
class ArtisansListView(generics.ListAPIView):
    queryset = Artisan.objects.all()
    serializer_class = ArtisanSerializer
    permission_classes = [AllowAny]



#Artisan registration views
class ArtisanRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        user_id = data.get('user_id')

        if not user_id or not str(user_id).isdigit():
            return Response({"error": "Invalid user ID format"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = int(user_id)

        if not User.objects.filter(id=user_id).exists():
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(id=user_id)

        required_fields = ['nin', 'location', 'experience', 'address', 'phone', 'service']
        for field in required_fields:
            if field not in data:
                return Response({"error": f"'{field}' is required"}, status=status.HTTP_400_BAD_REQUEST)

        data['user'] = user_id

        artisan_serializer = ArtisanSerializer(data=data)
        if artisan_serializer.is_valid():
            artisan = artisan_serializer.save()
            if 'profile_img' in request.FILES:
                artisan.profile_img = request.FILES['profile_img']
                artisan.save()

            user.is_artisan = True
            user.save()

            return Response(artisan_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(artisan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# api/views.py
class ArtisansByServiceView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, service_title):
        response_data = {'service_title': service_title}

        
        try:
            service = Service.objects.get(title=service_title)
            artisans = Artisan.objects.filter(service=service)
            serializer = ArtisanSerializer(artisans, many=True)

            

            #print('product and services we offer',service)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        
        except Service.DoesNotExist:
            response_data['error'] = 'Service not found'
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            #return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)




#Artisan search/filter view
class ArtisanSearchListView(generics.ListAPIView):
    serializer_class = ArtisanSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Artisan.objects.all()
        service = self.request.query_params.get('service', None) 
        location = self.request.query_params.get('location', None) 
        job_type = self.request.query_params.get('job_type', None) 
        industry = self.request.query_params.get('industry', None) 
        
        if service:
            queryset = queryset.filter(service__title__icontains=service) 
        if location:
            queryset = queryset.filter(location__id=location) 
        if job_type:
            queryset = queryset.filter(job_type__icontains=job_type) 
        if industry:
            queryset = queryset.filter(industry__name__icontains=industry) 
        
        return queryset

