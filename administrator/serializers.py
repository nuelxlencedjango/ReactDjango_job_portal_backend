# serializers.py
from rest_framework import serializers
from acct.models import ArtisanProfile

class ArtisanProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username')  # Access the username from the related CustomUser
    email = serializers.CharField(source='user.email')    # Access the email from the related CustomUser

    class Meta:
        model = ArtisanProfile
        fields = ['id','name','email','phone_number','service','experience','location',
                'profile_image',
                ]






from django.contrib.auth import get_user_model

User = get_user_model()

class ArtisanProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # to show the associated user's username

    class Meta:
        model = ArtisanProfile
        fields = ['id', 'user', 'phone_number', 'address', 'service', 'experience', 'profile_image', 'nin', 'job_type', 'industry', 'pay']




