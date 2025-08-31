from rest_framework import serializers
from .models import *
from acct.models import CustomUser, ArtisanProfile

from api.models import Area
from cloudinary.utils import cloudinary_url

from rest_framework import serializers
from .models import Order, OrderItem  


#checkout 
class CheckoutSerializer(serializers.ModelSerializer): 
    class Meta:
       # model = Checkout 
        fields = ['id', 'user', 'full_name', 'email', 'phone']



class JobDetailsSerializer(serializers.ModelSerializer):
    employer = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)
    artisan = serializers.CharField()  # Artisan is treated as text (CharField)
    location = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())  

    class Meta:
        model = JobDetails
        fields = [
            'id', 'employer', 'description', 'artisan', 'address',
            'contact_person', 'contact_person_phone', 'expectedDate',
            'location']
        read_only_fields = ['date_created', 'added_at']

    def validate_contact_person_phone(self, value):
        """Validate the phone number."""
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must be numeric.")
        if len(value) < 10 or len(value) > 11:
            raise serializers.ValidationError("Phone number must be between 11 digits.")
        return value






class ArtisanDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    location = serializers.CharField(source="location.location", read_only=True)
    service = serializers.CharField(source="service.title", read_only=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = ArtisanProfile
        fields = ['id', 'first_name', 'last_name', 'location', 'pay', 'profile_image', 'experience', 'service']

    def get_profile_image(self, obj):
        if obj.profile_image:
            # Generate resized URL using Cloudinary transformations
            return cloudinary_url(obj.profile_image.public_id,width=300,height=300,crop="fill",
                quality="auto",fetch_format="auto")[0]
        return None



class CartItemSerializer(serializers.ModelSerializer):
    artisan = ArtisanDetailSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'artisan', 'added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_code', 'paid', 'created_at', 'modified_at', 'items']



class ServicesRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','user','order_code','total_price','cart_code','status','paid_at', 
            'paid',]
        
        read_only_fields = ['id', 'order_code', 'paid_at']   

    def to_representation(self, instance):
       
        representation = super().to_representation(instance)
        representation['paid_at'] = instance.paid_at.strftime("%Y-%m-%d %H:%M:%S") 
        return representation
    



class TransactionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetails
        fields = ['tx_ref', 'cart', 'total_amount', 'transaction_id', 'status', 'modified_at']






class OrderItemSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id','artisan','artisan_name','service','service_name','price','total']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id','order_code','total_price','order_status','payment_status',
                  'paid','paid_at','items']
        read_only_fields = fields


