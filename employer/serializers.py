from rest_framework import serializers
from .models import *
from acct.models import CustomUser, ArtisanProfile
from acct.serializers import CustomUserSerializer,EmployerProfileSerializer
from api.models import Area












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







from rest_framework import serializers
from .models import CartItem, Cart

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
        return obj.profile_image.url if obj.profile_image else None

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




