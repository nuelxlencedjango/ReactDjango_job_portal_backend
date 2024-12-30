from rest_framework import serializers
from .models import *
from acct.models import CustomUser, ArtisanProfile
from acct.serializers import CustomUserSerializer,EmployerProfileSerializer
from api.models import Area



#new
'''

#cart serializer and cart item
class CartItemSerializernn(serializers.ModelSerializer): 
    artisan_name = serializers.CharField(source="artisan.user.first_name", read_only=True)
    service_title = serializers.CharField(source="service.title", read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'artisan', 'artisan_name', 'service', 'service_title', 'quantity', 'added_at']

class CartSerializernn(serializers.ModelSerializer): 
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_code', 'paid', 'created_at', 'modified_at', 'items']



#cart item retrival
class CartItemSerializerll(serializers.ModelSerializer):
    artisan = serializers.SerializerMethodField()
    employer  = EmployerProfileSerializer()
    class Meta:
        model = CartItem 
        fields = ['id', 'artisan', 'added_at', 'employer']

    def get_artisan(self, obj):
        return {
            "id": obj.artisan.id,
            "first_name": obj.artisan.user.first_name,
            "last_name": obj.artisan.user.last_name,
            "profile_image": obj.artisan.profile_image.url if obj.artisan.profile_image else None,
            "location": obj.artisan.location.location if obj.artisan.location else None,
            "service": obj.artisan.service.title if obj.artisan.service else None,
            "pay": obj.artisan.pay,
        }
    


'''


from rest_framework import serializers
from .models import CartItem
from acct.models import ArtisanProfile  # Assuming ArtisanProfile is in the 'acct' app
from api.models import Service  # Assuming Service is in the 'api' app
from .serializers import EmployerProfileSerializer  # Assuming you have this serializer for employers

class CartItemSerializer(serializers.ModelSerializer):
    # Including artisan details
    artisan = serializers.SerializerMethodField()  # Custom method to fetch artisan data
    employer = EmployerProfileSerializer(read_only=True)  # Assuming you have an EmployerProfileSerializer
    
    class Meta:
        model = CartItem
        fields = ['id', 'artisan', 'added_at', 'employer', 'quantity']  # Add the fields you want in the response

    def get_artisan(self, obj):
        """Custom method to fetch detailed artisan data."""
        return {
            "id": obj.artisan.id,
            "first_name": obj.artisan.user.first_name,
            "last_name": obj.artisan.user.last_name,
            "profile_image": obj.artisan.profile_image.url if obj.artisan.profile_image else None,
            "location": obj.artisan.location.location if obj.artisan.location else None,
            "service": obj.artisan.service.title if obj.artisan.service else None,
            "pay": obj.artisan.pay,
        }



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Nested CartItemSerializer

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_code', 'paid', 'created_at', 'modified_at', 'items']


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
            'location'
        ]
        read_only_fields = ['date_created', 'added_at']

    def validate_contact_person_phone(self, value):
        """Validate the phone number."""
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must be numeric.")
        if len(value) < 10 or len(value) > 11:
            raise serializers.ValidationError("Phone number must be between 11 digits.")
        return value




