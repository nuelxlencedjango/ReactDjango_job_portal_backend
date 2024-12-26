from rest_framework import serializers
from api.models import *





class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
       
        fields = ['id', 'name']


class ServiceSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Service
       
        fields = ['id', 'title', 'icon', 'time', 'location', 'description', 'company', 'img']




class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id','location']


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id','name']






class ArtisanSearchListSerializer(serializers.ModelSerializer): 
    profile_img = serializers.SerializerMethodField()
   # user = UserSerializer()
    location = AreaSerializer()
    service = ServiceSerializer()
    #in_cart = serializers.SerializerMethodField()

    class Meta:
     #   model = Artisan
        fields = [
            'user', 'location', 'experience', 'service', 'profile_img', 'pay',
        ]
        read_only_fields = ['date_joined']

    def get_profile_img(self, obj):
        return obj.profile_img.url if obj.profile_img else None

    #def get_in_cart(self, obj):
        # Check if the artisan is in the user's cart
     #   cart_items = self.context.get('cart_items', [])
      #  return obj.id in cart_items

