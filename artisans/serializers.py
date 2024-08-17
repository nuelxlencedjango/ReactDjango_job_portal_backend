# serializers.py
from rest_framework import serializers
from .models import Area,Artisan,Profession
from accounts.serializers import UserSerializer,User
from api.serializers import ServiceSerializer
from api.models import Service

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id','location']


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id','name']



class ServiceSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    class Meta:
        model = Service
        fields = "__all__"

    def get_img(self, obj):
        if obj.img:
            return obj.img.url
        return None    




class jkArtisanSerializer(serializers.ModelSerializer):
   # user = UserSerializer() 
    location = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    profile_img = serializers.SerializerMethodField()

    class Meta:
        model = Artisan
        fields = ['user', 'nin', 'location', 'experience', 'address', 'phone', 'service', 'profile_img', 'date_joined']
        read_only_fields = ['date_joined']

    def get_profile_img(self, obj):
        if obj.profile_img:
            return obj.profile_img.url
        return None
    
    def get_location(self, obj):
        return {
            'id': obj.location.id,
            'location': obj.location.location
        } if obj.location else None

    def get_service(self, obj):
        return {
            'id': obj.service.id,
            'title': obj.service.title
        } if obj.service else None








class poArtisanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artisan
        fields = ['user', 'nin', 'location', 'experience', 'address', 'phone', 'service', 'profile_img', 'date_joined']
        read_only_fields = ['date_joined']

    location = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    profile_img = serializers.SerializerMethodField()

    def get_profile_img(self, obj):
        if obj.profile_img:
            return obj.profile_img.url
        return None




from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Service, Artisan
from .serializers import ArtisanSerializer

class ArtisansByServiceView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, service_title):
        try:
            service = Service.objects.get(title=service_title)
            artisans = Artisan.objects.filter(service=service)
            serializer = ArtisanSerializer(artisans, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Service.DoesNotExist:
            return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
