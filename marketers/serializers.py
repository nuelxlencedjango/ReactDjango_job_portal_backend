from rest_framework import serializers
from .models import *
from acct.models import ArtisanProfile
from acct.serializers import CustomUserSerializer 
from api.serializers import AreaSerializer,ServiceSerializer




class ArtisanSearchListSerializer(serializers.ModelSerializer): 
    profile_image = serializers.SerializerMethodField()
    user = CustomUserSerializer()
    location = AreaSerializer()
    service = ServiceSerializer()
 

    class Meta:
        model = ArtisanProfile
        fields = [
            'user', 'location', 'experience', 'service', 'profile_image', 'pay','marketer' 
        ]
        read_only_fields = ['date_joined']

    def get_profile_image(self, obj):
        return obj.profile_image.url if obj.profile_image else None



