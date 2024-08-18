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








class ArtisanSerializer(serializers.ModelSerializer):
    location = AreaSerializer()  # Use nested serializer
    service = ServiceSerializer() 
    class Meta:
        model = Artisan
        fields = ['user', 'nin', 'location', 'experience', 'address', 'phone', 'service', 'profile_img', 'date_joined']
        read_only_fields = ['date_joined']

    #location = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    #service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    profile_img = serializers.SerializerMethodField()

    def get_profile_img(self, obj):
        if obj.profile_img:
            return obj.profile_img.url
        return None


