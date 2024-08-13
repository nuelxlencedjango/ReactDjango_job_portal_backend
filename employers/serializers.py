from rest_framework import serializers
from .models import *
from accounts.serializers import UserSerializer




class EmployerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employer
        fields = ('user', 'phone_number')




class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'
