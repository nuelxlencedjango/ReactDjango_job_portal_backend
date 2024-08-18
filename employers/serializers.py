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





class OrderRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = ['employer', 'artisan', 'request_data', 'location','service','phone','pay']
        read_only_fields = ['employer', 'request_date']





class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = ['employer', 'area', 'description','job_date','phone_number','time','contact_person']
        read_only_fields = ['employer']
