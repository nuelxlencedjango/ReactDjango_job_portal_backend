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


