

# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ArtisanProfile, EmployerProfile, ManagerProfile

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