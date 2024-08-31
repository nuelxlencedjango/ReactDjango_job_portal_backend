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





class llOrderRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = ['id', 'employer', 'artisan', 'service', 'description', 'address', 'area', 'job_date', 'preferred_time', 'contact_person', 'phone_number']
        read_only_fields = ['date_ordered','paid']

    def create(self, validated_data):
        request = self.context.get('request')
        employer = request.user.employer 
        validated_data['employer'] = employer
        return super().create(validated_data)



from rest_framework import serializers
from .models import OrderRequest

class OrderRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = ['description', 'address', 'area', 'job_date', 'preferred_time', 'contact_person', 'phone_number', 'artisan', 'service', 'employer', 'date_ordered']
        read_only_fields = ['employer', 'date_ordered']
