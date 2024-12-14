# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser, ArtisanProfile, EmployerProfile




class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'user_type']
        extra_kwargs = {'password': {'write_only': True}, 'password2': {'write_only': True}}

    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def validate_email(self, value):
        # Ensure email is unique
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already taken.")
        return value

    def create(self, validated_data):
         # Remove confirm_password from the validated data since it's not needed for user creation 
        validated_data.pop('password2', None)

        # Create the user with the validated data
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            user_type=validated_data.get('user_type')  
            #user_type=validated_data.get('user_type', 'default_value')  
        )

        # Set and hash the password before saving
        user.set_password(validated_data['password'])
        user.save()

        return user





class hjjArtisanProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtisanProfile
        fields = ['experience', 'service', 'pay', 'profile_image', 'fingerprint_image', 'nin', 'phone_number', 'address']




from rest_framework import serializers
from .models import ArtisanProfile, CustomUser  # Ensure you import the right model

class AkoortisanProfileSerializer(serializers.ModelSerializer):
    # The 'user' field should be included and either required or read-only
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=True)

    class Meta:
        model = ArtisanProfile
        fields = ['user', 'experience', 'service', 'pay', 'profile_image', 'fingerprint_image', 'nin', 'phone_number', 'address']

    def create(self, validated_data):
        # Create the ArtisanProfile instance with the validated data
        return ArtisanProfile.objects.create(**validated_data)



class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_address']




from rest_framework import serializers
from .models import ArtisanProfile, CustomUser

class ArtisanProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=True)
    
    # You can add file validation here, if needed
    profile_image = serializers.ImageField(required=False)
    fingerprint_image = serializers.ImageField(required=False)

    class Meta:
        model = ArtisanProfile
        fields = ['user', 'experience', 'service', 'pay', 'profile_image', 'fingerprint_image', 'nin', 'phone_number', 'address']

    def create(self, validated_data):
        return ArtisanProfile.objects.create(**validated_data)
