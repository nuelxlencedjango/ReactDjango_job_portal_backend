# users/serializers.py
from rest_framework import serializers
#from django.contrib.auth import get_user_model
from .models import CustomUser, ArtisanProfile, EmployerProfile, MarketerProfile
from .models import Fingerprint 






class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'user_type']
        extra_kwargs = {'password': {'write_only': True}, 'password2': {'write_only': True}}

    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")

        # manager with user_type='manager' not allowed to register
        if data.get('user_type') == 'manager' or data.get('user_type') == 'marketer':
            raise serializers.ValidationError("Managers cannot be created through this endpoint.")
        return data

    def validate_email(self, value):
        # Ensure email is unique
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already taken.")
        return value

    def create(self, validated_data):
        # Remove confirm_password from the validated data since it's not needed for user creation
        validated_data.pop('password2', None)

        # Create the user with the validated data
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'].capitalize(),
            last_name=validated_data['last_name'].capitalize(),
            email=validated_data['email'],
            user_type=validated_data.get('user_type')
        )

        # Set and hash the password before saving
        user.set_password(validated_data['password'])
        user.save()

        return user




from rest_framework import serializers
from cloudinary.uploader import upload
import cloudinary.utils
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import ArtisanProfile, CustomUser, MarketerProfile

class ArtisanProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=True)
    marketer = serializers.PrimaryKeyRelatedField(queryset=MarketerProfile.objects.all(), required=False, allow_null=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)
    profile_image_resized = serializers.SerializerMethodField()

    class Meta:
        model = ArtisanProfile
        fields = [
            'user', 'experience', 'location', 'service', 'pay',
            'profile_image', 'profile_image_resized', 'nin', 'phone_number',
            'address', 'date_joined', 'marketer'
        ]
        read_only_fields = ['date_joined']

    def get_profile_image_resized(self, obj):
        """Returns a resized version of the profile image using Cloudinary transformations."""
        if obj.profile_image:
            return cloudinary.utils.cloudinary_url(
                obj.profile_image.public_id,
                width=300,
                height=300,
                crop="fit",
                quality="auto",
                fetch_format="auto"
            )[0]  # Returns the URL
        return None

    def process_and_upload_image(self, image):
        """Resizes the image if it's too large and uploads it to Cloudinary."""
        max_size = 5 * 1024 * 1024  # 5MB limit
        max_resolution = (800, 800)  # Resize to max 800x800

        try:
            # Convert to PIL image
            img = Image.open(image)
            img_format = img.format  # Preserve original format

            # Resize if image is too large
            if image.size > max_size or img.size[0] > max_resolution[0] or img.size[1] > max_resolution[1]:
                img.thumbnail(max_resolution)  # Resize while maintaining aspect ratio

                # Save to a BytesIO stream
                img_io = BytesIO()
                img.save(img_io, format=img_format)
                img_io.seek(0)

                # Convert back to Django InMemoryUploadedFile
                image = InMemoryUploadedFile(
                    img_io, None, image.name, f"image/{img_format.lower()}", img_io.tell(), None
                )

            # Upload to Cloudinary
            uploaded_image = upload(
                image,
                quality="auto",
                fetch_format="auto"
            )
            return uploaded_image['public_id']  # Store the Cloudinary public_id

        except Exception as e:
            raise serializers.ValidationError(f"Failed to process image: {str(e)}")

    def create(self, validated_data):
        """Create an ArtisanProfile instance with the processed profile image."""
        profile_image = validated_data.pop('profile_image', None)
        artisan = ArtisanProfile.objects.create(**validated_data)
        if profile_image:
            artisan.profile_image = self.process_and_upload_image(profile_image)
            artisan.save()
        return artisan

    def update(self, instance, validated_data):
        """Update an ArtisanProfile instance with the processed profile image."""
        profile_image = validated_data.pop('profile_image', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if profile_image:
            instance.profile_image = self.process_and_upload_image(profile_image)
        instance.save()
        return instance





class EmployerProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=True)
    class Meta:
        model = EmployerProfile
        fields = ['user','company_name','phone_number','location']
        read_only_fields = ['date_joined']
 
    def create(self, validated_data):
        return EmployerProfile.objects.create(**validated_data)






class FingerprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fingerprint
        fields = ['id', 'artisan_profile', 'fingerprint_image', 'created_at']
        read_only_fields = ['created_at']

    def validate_fingerprint_image(self, value):
        # Check if the image is provided and its format is valid
        if value is None:
            raise serializers.ValidationError("No image provided.")
        
       
        if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise serializers.ValidationError("Invalid image format. Only PNG, JPG, or JPEG are allowed.")
        
        return value
