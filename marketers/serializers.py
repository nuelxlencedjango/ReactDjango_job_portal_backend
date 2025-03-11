from acct.models import CustomUser,ArtisanProfile,MarketerProfile
from rest_framework import serializers

class ArtisanProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=True)
    marketer = serializers.PrimaryKeyRelatedField(queryset=MarketerProfile.objects.all(), required=False, allow_null=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = ArtisanProfile
        fields = [
            'user', 'experience', 'location', 'service', 'pay', 'profile_image', 
            'nin', 'phone_number', 'address', 'date_joined', 'marketer' 
        ]
        read_only_fields = ['date_joined']

    def get_profile_image(self, obj):
        """Returns the URL of the profile image, if it exists."""
        if obj.profile_image:
            return obj.profile_image.url
        return None

    def create(self, validated_data):
        """Create an ArtisanProfile instance."""
        return ArtisanProfile.objects.create(**validated_data)