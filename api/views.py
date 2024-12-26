
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from rest_framework import generics,status
from rest_framework.response import Response
from acct.models import ArtisanProfile
from .models import *
from .serializers import ServiceSerializer,IndustrySerializer,AreaSerializer,ProfessionSerializer,ArtisanSearchListSerializer
#from artisans.models import *
#from artisans.serializers import *



class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
   


class IndustryListView(generics.ListAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [AllowAny]



#list Area objects
class AreaListView(generics.ListAPIView):
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






'''

#list Artisans objects
class ArtisansListView(generics.ListAPIView):
   # queryset = Artisan.objects.all()
    serializer_class = ArtisanSerializer
    permission_classes = [AllowAny]


#create/add location/areas
class AreaCreateView(generics.CreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [AllowAny]



#create /add profess
class ProfessionCreateView(generics.CreateAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    permission_classes = [AllowAny]

'''




# api/views.py
class ArtisansByServiceView(APIView): 
    permission_classes = [AllowAny]
    def get(self, request, service_title):
        response_data = {'service_title': service_title}
    
        
        try:
            service = Service.objects.get(title=service_title)
            artisans = ArtisanProfile.objects.filter(service=service)
            serializer = ArtisanSearchListSerializer(artisans, many=True)

            #print('product and services we offer',service)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        
        except Service.DoesNotExist:
            response_data['error'] = 'Service not found'
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)