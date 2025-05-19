# users/serializers.py
from rest_framework import serializers
from .models import Fingerprint 
from django.core.files.images import ImageFile
from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User

from .models import CustomUser, ArtisanProfile, EmployerProfile, ManagerProfile, MarketerProfile
from cloudinary.utils import cloudinary_url



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

        # manager with user_type='manager' not allowed to register
        if data.get('user_type') == 'manager' or data.get('user_type') == 'marketer':
            raise serializers.ValidationError("Managers cannot be created through this endpoint.")
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
        )

        # Set and hash the password before saving
        user.set_password(validated_data['password'])
        user.save()

        return user



class ArtisanProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=True)
    marketer = serializers.PrimaryKeyRelatedField(queryset=MarketerProfile.objects.all(), required=False, allow_null=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)
    profile_image_resized = serializers.SerializerMethodField()

    class Meta:
        model = ArtisanProfile
        fields = [
            'user', 'experience', 'location', 'service', 'pay',
            'profile_image', 'profile_image_resized', 'nin', 'phone_number',
            'address', 'date_joined', 'marketer'
        ]
        read_only_fields = ['date_joined']

    def get_profile_image_resized(self, obj):
        """Returns a resized version of the profile image using Cloudinary transformations."""
        if obj.profile_image:
            # Generate a resized image URL (e.g., 300x300) using Cloudinary
            return cloudinary_url(
                obj.profile_image.public_id,
                width=300,
                height=300,
                crop="fit",
                quality="auto",
                fetch_format="auto"
            )[0]  # Returns the URL
        return None

    def validate_profile_image(self, value):
        """Validate the image file."""
        if value:
            max_size = 5 * 1024 * 1024  # 5MB limit
            if value.size > max_size:
                raise serializers.ValidationError("Image size must be less than 5MB.")
            try:
                # Verify the file is an image
                from PIL import Image
                Image.open(value).verify()
            except Exception:
                raise serializers.ValidationError("Invalid image file.")
        return value

    def create(self, validated_data):
        """Create an ArtisanProfile instance with the processed profile image."""
        profile_image = validated_data.pop('profile_image', None)
        artisan = ArtisanProfile.objects.create(**validated_data)
        if profile_image:
            artisan.profile_image = profile_image
            artisan.save()  # The model's save() method will handle resizing
        return artisan

    def update(self, instance, validated_data):
        """Update an ArtisanProfile instance with the processed profile image."""
        profile_image = validated_data.pop('profile_image', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if profile_image:
            instance.profile_image = profile_image
        instance.save()  # The model's save() method will handle resizing
        return instance


class EmployerProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=True)
    class Meta:
        model = EmployerProfile
        fields = ['user','company_name','phone_number','location']
        read_only_fields = ['date_joined']
 
    def create(self, validated_data):
        return EmployerProfile.objects.create(**validated_data)






class FingerprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fingerprint
        fields = ['id', 'artisan_profile', 'fingerprint_image', 'created_at']
        read_only_fields = ['created_at']

    def validate_fingerprint_image(self, value):
        # Check if the image is provided and its format is valid
        if value is None:
            raise serializers.ValidationError("No image provided.")
        
       
        if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise serializers.ValidationError("Invalid image format. Only PNG, JPG, or JPEG are allowed.")
        
        return value






class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField('username')
    first_name = serializers.CharField('first_name', allow_null=True)
    last_name = serializers.CharField('last_name', allow_null=True)
    user_type = serializers.CharField('user_type')
    company_name = serializers.SerializerMethodField()
    company_logo = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'user_type', 'company_name', 'company_logo']

    def get_company_name(self, obj):
        try:
            if obj.user_type == 'employer':
                profile = EmployerProfile.objects.get(user=obj)
                return profile.company_name
            return None
        except EmployerProfile.DoesNotExist:
            return None

    def get_company_logo(self, obj):
        try:
            if obj.user_type == 'artisan':
                profile = ArtisanProfile.objects.get(user=obj)
                return profile.profile_image.url if profile.profile_image else None
            
            elif obj.user_type == 'marketer':
                profile = MarketerProfile.objects.get(user=obj)
                return profile.profile_image.url if profile.profile_image else None
            
            elif obj.user_type == 'manager':
                profile = ManagerProfile.objects.get(user=obj)
                return profile.profile_image.url if profile.profile_image else None
            
            return None
        except CustomUser.DoesNotExist:
            return None
        
    
  