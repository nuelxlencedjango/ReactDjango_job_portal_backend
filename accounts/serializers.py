
from rest_framework import serializers
from .models import User
from artisans.models import *
from employers.models import *

from django.contrib.auth import get_user_model, authenticate


User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'is_artisan', 'is_employer')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            
        )
      
        user.set_password(password)
        user.save()
        return user

from rest_framework import serializers
from django.contrib.auth.models import User

class hjUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'is_artisan', 'is_employer')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extract password and other fields
        password = validated_data.pop('password')
        is_artisan = validated_data.pop('is_artisan', False)
        is_employer = validated_data.pop('is_employer', False)
        
        # Create the user
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        
        # Set custom flags
        user.is_artisan = is_artisan
        user.is_employer = is_employer
        
        # Save the user
        user.save()
        return user
