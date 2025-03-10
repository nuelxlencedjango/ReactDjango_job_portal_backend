# users/serializers.py
from rest_framework import serializers
#from django.contrib.auth import get_user_model
from .models import CustomUser, ArtisanProfile, EmployerProfile, MarketerProfile
from .models import Fingerprint 






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
        if data.get('user_type') == 'manager':
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
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = ArtisanProfile
        fields = [
            'user', 'experience', 'location', 'service', 'pay', 'profile_image', 
            'nin', 'phone_number', 'address', 'date_joined', 'marketer'
        ]
        read_only_fields = ['date_joined']

    def get_profile_image(self, obj):
        """Returns the URL of the profile image, if it exists."""
        if obj.profile_image:
            return obj.profile_image.url
        return None

    def create(self, validated_data):
        """Create an ArtisanProfile instance."""
        return ArtisanProfile.objects.create(**validated_data)




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
