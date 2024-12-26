
from rest_framework import serializers
#from .models import User
#from artisans.models import *
from employers.models import *

from django.contrib.auth import get_user_model, authenticate

'''

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
'''
    



from rest_framework import serializers
from django.contrib.auth import get_user_model
#from .models import ArtisanProfile, EmployerProfile, ManagerProfile

User = get_user_model()

class zmRegistrationSerializer(serializers.ModelSerializer):
    # This assumes that 'user_type' is one of the choices ('admin', 'manager', 'employer', 'artisan')
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'password', 'confirm_password']
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        user_data = validated_data
        password = user_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()

        # Create user profile based on user_type
        if user.user_type == 'artisan':
            ArtisanProfile.objects.create(user=user)
        elif user.user_type == 'employer':
            EmployerProfile.objects.create(user=user)
        elif user.user_type == 'manager':
            ManagerProfile.objects.create(user=user)

        return user




from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class ieeRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'password', 'confirm_password']
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        user_data = validated_data
        password = user_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()

        # Signal will automatically create the profile based on user_type
        return user



# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
#from .models import ArtisanProfile, EmployerProfile, ManagerProfile

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'password', 'confirm_password']
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        # Extract password and create user
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Make sure password is hashed
        user.save()

        # Create profile based on user type
        if user.user_type == 'artisan':
            ArtisanProfile.objects.create(user=user)
        elif user.user_type == 'employer':
            EmployerProfile.objects.create(user=user)
        elif user.user_type == 'manager':
            ManagerProfile.objects.create(user=user)

        return user
