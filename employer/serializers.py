from rest_framework import serializers
from .models import *
from acct.models import CustomUser, ArtisanProfile
from acct.serializers import CustomUserSerializer,EmployerProfileSerializer
from api.models import Area


from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

    











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





class ArtisanDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    location = serializers.CharField(source="location.location", read_only=True)
    service = serializers.CharField(source="service.title", read_only=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = ArtisanProfile
        fields = ['id', 'first_name', 'last_name', 'location', 'pay', 'profile_image', 'experience', 'service']

    #def get_profile_image(self, obj):
     #   return obj.profile_image.url if obj.profile_image else None
    
    def get_profile_image(self, obj):
        if obj.profile_image:
            # Open the image using Pillow
            img = Image.open(obj.profile_image)
            # Resize the image (e.g., to 200x200)
            img.thumbnail((200, 200))
            # Save the resized image to a BytesIO buffer
            buffer = BytesIO()
            img.save(buffer, format='JPEG')
            # Save the resized image back to the profile_image field
            obj.profile_image.save(obj.profile_image.name, ContentFile(buffer.getvalue()), save=False)
            obj.save()
            return obj.profile_image.url
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





class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'order_code',
            'total_price',
            'cart_code',
            'status',
            'paid_at',
            'paid',
        ]
        read_only_fields = ['id', 'order_code', 'paid_at']  

    def to_representation(self, instance):
       
        representation = super().to_representation(instance)
        representation['paid_at'] = instance.paid_at.strftime("%Y-%m-%d %H:%M:%S") 
        return representation