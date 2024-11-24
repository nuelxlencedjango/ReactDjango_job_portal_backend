from rest_framework import serializers
from .models import Cart, CartItem,Employer,JobPost,Order,OrderRequest
from accounts.serializers import UserSerializer



#new
#cart serializer and cart item
class CartItemSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source="artisan.user.first_name", read_only=True)
    service_title = serializers.CharField(source="service.title", read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'artisan', 'artisan_name', 'service', 'service_title', 'quantity', 'added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_code', 'paid', 'created_at', 'modified_at', 'items']



#cart item retrival
class CartItemSerializer(serializers.ModelSerializer):
    artisan = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'artisan', 'added_at']

    def get_artisan(self, obj):
        return {
            "id": obj.artisan.id,
            "first_name": obj.artisan.user.first_name,
            "last_name": obj.artisan.user.last_name,
            "profile_img": obj.artisan.profile_img.url if obj.artisan.profile_img else None,
            "location": obj.artisan.location.location if obj.artisan.location else None,
            "service": obj.artisan.service.title if obj.artisan.service else None,
            "pay": obj.artisan.pay,
        }






class EmployerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employer
        fields = ('user', 'phone_number')




class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'







from rest_framework import serializers
from .models import OrderRequest

class OrderRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = ['description', 'address', 'area', 'job_date', 'preferred_time', 'contact_person', 'phone_number', 'artisan', 'service', 'employer', 'date_ordered']
        read_only_fields = ['employer', 'date_ordered']
