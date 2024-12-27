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
            first_name=validated_data['first_name'].capitalize(),
            last_name=validated_data['last_name'].capitalize(),
            email=validated_data['email'],
            user_type=validated_data.get('user_type')  
            #user_type=validated_data.get('user_type', 'default_value')  
        )

        # Set and hash the password before saving
        user.set_password(validated_data['password'])
        user.save()

        return user









class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = ['company_name']






from rest_framework import serializers
from .models import ArtisanProfile, CustomUser

class ArtisanProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=True)
    
    # Custom fields to get URLs for the images
    profile_image = serializers.SerializerMethodField() 
   # fingerprint_image = serializers.SerializerMethodField()

    class Meta:
        model = ArtisanProfile
        fields = ['user', 'experience','location', 'service', 'pay', 'profile_image', 'nin', 
                  'phone_number', 'address', 'date_joined']
        read_only_fields = ['date_joined']

    def get_profile_image_url(self, obj):
        """Returns the URL of the profile image, if it exists."""
        if obj.profile_image: 
            return obj.profile_image.url 
        return None

 

    def create(self, validated_data):
        return ArtisanProfile.objects.create(**validated_data)






# serializers.py
from rest_framework import serializers
from .models import Fingerprint

class FingerprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fingerprint
        fields = ['id', 'artisan_profile', 'fingerprint_image', 'fingerprint_template', 'created_at']
        read_only_fields = ['created_at']

    def validate_fingerprint_image(self, value):
        # Add validation if needed (e.g., image size, type)
        if value.size > 5 * 1024 * 1024:  # Limit size to 5 MB
            raise serializers.ValidationError("Image size is too large")
        return value
