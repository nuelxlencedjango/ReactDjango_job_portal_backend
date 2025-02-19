from rest_framework import serializers
from .models import *
from acct.models import ArtisanProfile
from acct.serializers import CustomUserSerializer 




class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
       
        fields = ['id', 'name']


class ServiceSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    class Meta:
        model = Service
       
        fields = ['id', 'title', 'icon', 'time', 'location', 'description', 'company', 'img']

    def get_img(self, obj):
        return obj.img.url if obj.img else None


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id','location']


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id','name']






class ArtisanSearchListSerializer(serializers.ModelSerializer): 
    profile_image = serializers.SerializerMethodField()
    user = CustomUserSerializer()
    location = AreaSerializer()
    service = ServiceSerializer()
    #in_cart = serializers.SerializerMethodField()

    class Meta:
        model = ArtisanProfile
        fields = [
            'user', 'location', 'experience', 'service', 'profile_image', 'pay', 
        ]
        read_only_fields = ['date_joined']

    def get_profile_image(self, obj):
        return obj.profile_image.url if obj.profile_image else None

    #def get_in_cart(self, obj):
        # Check if the artisan is in the user's cart
     #   cart_items = self.context.get('cart_items', [])
      #  return obj.id in cart_items

