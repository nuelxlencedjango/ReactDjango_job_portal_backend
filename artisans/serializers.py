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




class hjkArtisanSerializer(serializers.ModelSerializer):
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
    profile_img = serializers.SerializerMethodField()

    class Meta:
        model = Artisan
        fields = ['user', 'nin', 'location', 'experience', 'address', 'phone', 'service', 'profile_img', 'date_joined']
        read_only_fields = ['date_joined']

    def __init__(self, *args, **kwargs):
        super(ArtisanSerializer, self).__init__(*args, **kwargs)
        request_method = self.context.get('request').method if self.context.get('request') else None

        if request_method in ['GET']:
            # Using nested serializers for fetching (GET request)
            self.fields['location'] = AreaSerializer()
            self.fields['service'] = ServiceSerializer()
            user = UserSerializer()
        else:
            # Using primary key related fields for creating/updating (POST, PUT, PATCH requests)
            self.fields['location'] = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
            self.fields['service'] = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
            #self.fields['user'] = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def get_profile_img(self, obj):
        if obj.profile_img:
            return obj.profile_img.url
        return None






class ArtisanSearchListSerializer(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()
    user = UserSerializer()  # Include user details in the response
    location = AreaSerializer()  # Nested Location Serializer
    service = ServiceSerializer()  # Nested Service Serializer

    class Meta:
        model = Artisan
        fields = [
            'user', 'location', 'experience',
            'service', 'profile_img', 'pay',
        ]
        read_only_fields = ['date_joined']

    def get_profile_img(self, obj):
        return obj.profile_img.url if obj.profile_img else None


