# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ArtisanProfile, EmployerProfile, ManagerProfile

User = get_user_model()






from rest_framework import serializers
from .models import CustomUser, ArtisanProfile, EmployerProfile

class rtCustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True) 

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password','first_name','last_name',]

    def validate(self, data):
        if data['password'] != data['confirm_password']: 
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class poArtisanProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtisanProfile
        fields = ['experience', 'service', 'pay', 'profile_image', 'fingerprint_image', 'nin','phone_number','address']

class ppEmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_address']








class CpoustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    #confirm_password = serializers.CharField(write_only=True) 

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            )
      
        user.set_password(password)
        user.save()
        return user






class CaqustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
   # confirm_password = serializers.CharField(write_only=True) 

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

   # def validate(self, data):
        # Check if passwords match
    #    if data['password'] != data['confirm_password']: 
     #       raise serializers.ValidationError("Passwords do not match.")
      #  return data

    def validate_email(self, value):
        # Ensure email is unique
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already taken.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            user_type=validated_data.get('user_type', 'default_value') 
        )

        user.set_password(password)
        user.save()
        return user




from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'user_type']
        extra_kwargs = {'password': {'write_only': True}, 'confirm_password': {'write_only': True}}

    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def validate_email(self, value):
        # Ensure email is unique
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already taken.")
        return value

    def create(self, validated_data):
        # Remove confirm_password from the validated data since it's not needed for user creation
        validated_data.pop('confirm_password', None)

        # Create the user with the validated data
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            user_type=validated_data.get('user_type', 'default_value')  # Default value if user_type is not provided
        )

        # Set and hash the password before saving
        user.set_password(validated_data['password'])
        user.save()

        return user






class ArtisanProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtisanProfile
        fields = ['experience', 'service', 'pay', 'profile_image', 'fingerprint_image', 'nin', 'phone_number', 'address']


class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_address']
