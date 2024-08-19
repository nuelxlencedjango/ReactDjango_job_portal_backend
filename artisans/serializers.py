# serializers.py
from rest_framework import serializers
from .models import Area,Artisan,Profession
from accounts.serializers import UserSerializer,User
from api.serializers import ServiceSerializer
from api.models import Service

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id','location']


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id','name']



class ServiceSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    class Meta:
        model = Service
        fields = "__all__"

    def get_img(self, obj):
        if obj.img:
            return obj.img.url
        return None    




class ArtisanSerializer(serializers.ModelSerializer):
   # user = UserSerializer() 
    location = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    profile_img = serializers.SerializerMethodField()

    class Meta:
        model = Artisan
        fields = ['user', 'nin', 'location', 'experience', 'address', 'phone', 'service', 'profile_img', 'date_joined']
        read_only_fields = ['date_joined']

    def get_profile_img(self, obj):
        if obj.profile_img:
            return obj.profile_img.url
        return None
    
    def get_location(self, obj):
        return {
            'id': obj.location.id,
            'location': obj.location.location
        } if obj.location else None

    def get_service(self, obj):
        return {
            'id': obj.service.id,
            'title': obj.service.title
        } if obj.service else None








class uiArtisanSerializer(serializers.ModelSerializer):
    location = AreaSerializer()  # Use nested serializer
    service = ServiceSerializer() 
    class Meta:
        model = Artisan
        fields = ['user', 'nin', 'location', 'experience', 'address', 'phone', 'service', 'profile_img', 'date_joined']
        read_only_fields = ['date_joined']

    #location = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    #service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    profile_img = serializers.SerializerMethodField()

    def get_profile_img(self, obj):
        if obj.profile_img:
            return obj.profile_img.url
        return None


class ArtisanSerializer(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()

    class Meta:
        model = Artisan
        fields = ['user', 'nin', 'location', 'experience', 'address', 'phone', 'service', 'profile_img', 'date_joined']
        read_only_fields = ['date_joined']

    def __init__(self, *args, **kwargs):
        super(ArtisanSerializer, self).__init__(*args, **kwargs)
        request_method = self.context.get('request').method if self.context.get('request') else None

        if request_method in ['GET']:
            # Using nested serializers for fetching (GET request)
            self.fields['location'] = AreaSerializer()
            self.fields['service'] = ServiceSerializer()
            user = UserSerializer()
        else:
            # Using primary key related fields for creating/updating (POST, PUT, PATCH requests)
            self.fields['location'] = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
            self.fields['service'] = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
            #self.fields['user'] = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def get_profile_img(self, obj):
        if obj.profile_img:
            return obj.profile_img.url
        return None






class AlprtisanSerializer(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Artisan
        fields = ['user', 'nin', 'location', 'experience', 'address', 'phone', 'service', 'profile_img', 'date_joined']
        read_only_fields = ['date_joined', 'user']

    def __init__(self, *args, **kwargs):
        super(ArtisanSerializer, self).__init__(*args, **kwargs)
        request_method = self.context.get('request').method if self.context.get('request') else None

        if request_method in ['GET']:
            # Nested serializers for GET requests
            self.fields['location'] = AreaSerializer()
            self.fields['service'] = ServiceSerializer()
        else:
            # PrimaryKeyRelatedField for POST/PUT requests
            self.fields['location'] = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
            self.fields['service'] = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())

    def get_profile_img(self, obj):
        return obj.profile_img.url if obj.profile_img else None




class AwartisanSerializer(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Artisan
        fields = ['user', 'nin', 'location', 'experience', 'address', 'phone', 'service', 'profile_img', 'date_joined']
        read_only_fields = ['date_joined']

    def __init__(self, *args, **kwargs):
        super(ArtisanSerializer, self).__init__(*args, **kwargs)
        request_method = self.context.get('request').method if self.context.get('request') else None

        if request_method == 'GET':
            self.fields['location'] = AreaSerializer()
            self.fields['service'] = ServiceSerializer()
        else:
            self.fields['location'] = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
            self.fields['service'] = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())

    def create(self, validated_data):
        # Extract the nested user data
        user_data = validated_data.pop('user')
        
        # Create the user
        user_data['is_artisan'] = True  # Ensure the is_artisan flag is set
        user = UserSerializer().create(user_data)
        
        # Create the artisan
        artisan = Artisan.objects.create(user=user, **validated_data)
        
        return artisan

    def get_profile_img(self, obj):
        return obj.profile_img.url if obj.profile_img else None
    





class djArtisanSerializer(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Artisan
        fields = [
            'user', 'nin', 'location', 'experience', 'address', 
            'phone', 'service', 'profile_img', 'date_joined'
        ]
        read_only_fields = ['date_joined']

    def __init__(self, *args, **kwargs):
        super(ArtisanSerializer, self).__init__(*args, **kwargs)
        request_method = self.context.get('request').method if self.context.get('request') else None

        if request_method == 'GET':
            # Use SerializerMethodField for dynamic data representation
            self.fields['location'] = serializers.SerializerMethodField()
            self.fields['service'] = serializers.SerializerMethodField()
        else:
            self.fields['location'] = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
            self.fields['service'] = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['is_artisan'] = True
        user = UserSerializer().create(user_data)
        artisan = Artisan.objects.create(user=user, **validated_data)
        return artisan

    def get_profile_img(self, obj):
        return obj.profile_img.url if obj.profile_img else None

    def get_location(self, obj):
        return {
            'id': obj.location.id,
            'location': obj.location.location
        } if obj.location else None

    def get_service(self, obj):
        return {
            'id': obj.service.id,
            'title': obj.service.title
        } if obj.service else None






class plArtisanSerializer(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()
    user = UserSerializer()
    location = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()

    class Meta:
        model = Artisan
        fields = [
            'user', 'nin', 'location', 'experience', 'address', 
            'phone', 'service', 'profile_img', 'date_joined'
        ]
        read_only_fields = ['date_joined']

    def __init__(self, *args, **kwargs):
        super(ArtisanSerializer, self).__init__(*args, **kwargs)
        request_method = self.context.get('request').method if self.context.get('request') else None

        if request_method != 'GET':
            # For non-GET requests, replace the location and service fields with PrimaryKeyRelatedField
            self.fields['location'] = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
            self.fields['service'] = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
            

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['is_artisan'] = True
        user = UserSerializer().create(user_data)
        artisan = Artisan.objects.create(user=user, **validated_data)
        return artisan

    def get_profile_img(self, obj):
        return obj.profile_img.url if obj.profile_img else None

    def get_location(self, obj):
        return {
            'id': obj.location.id,
            'location': obj.location.location
        } if obj.location else None

    def get_service(self, obj):
        return {
            'id': obj.service.id,
            'title': obj.service.title
        } if obj.service else None





class poArtisanSerializer(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()
    user = UserSerializer()
    location = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()

    class Meta:
        model = Artisan
        fields = [
            'user', 'nin', 'location', 'experience', 'address', 
            'phone', 'service', 'profile_img', 'date_joined'
        ]
        read_only_fields = ['date_joined']

    def get_profile_img(self, obj):
        return obj.profile_img.url if obj.profile_img else None

    def get_location(self, obj):
        if obj.location:
            return {
                'id': obj.location.id,
                'location': obj.location.location
            }
        return None

    def get_service(self, obj):
        if obj.service:
            return {
                'id': obj.service.id,
                'title': obj.service.title
            }
        return None

    '''
      def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['is_artisan'] = True
        user = UserSerializer().create(user_data)
        artisan = Artisan.objects.create(user=user, **validated_data)
        return artisan
    '''

class nnArtisanSerializer(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()
    user = UserSerializer(required=False)  # Make user optional by default
    location = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()

    class Meta:
        model = Artisan
        fields = [
            'user', 'nin', 'location', 'experience', 'address', 
            'phone', 'service', 'profile_img', 'date_joined'
        ]
        read_only_fields = ['date_joined']

    def __init__(self, *args, **kwargs):
        super(ArtisanSerializer, self).__init__(*args, **kwargs)
        request_method = self.context.get('request').method if self.context.get('request') else None

        if request_method == 'POST':
            self.fields['user'].required = False  # Set user to optional for POST requests
             # Using primary key related fields for creating/updating (POST, PUT, PATCH requests)
            self.fields['location'] = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
            self.fields['service'] = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())

    def get_profile_img(self, obj):
        return obj.profile_img.url if obj.profile_img else None

    def get_location(self, obj):
        if obj.location:
            return {
                'id': obj.location.id,
                'location': obj.location.location
            }
        return None

    def get_service(self, obj):
        if obj.service:
            return {
                'id': obj.service.id,
                'title': obj.service.title
            }
        return None



class ssArtisanSerializer(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()
    user = UserSerializer(required=False)  # Make user optional by default

    class Meta:
        model = Artisan
        fields = [
            'user', 'nin', 'location', 'experience', 'address', 
            'phone', 'service', 'profile_img', 'date_joined'
        ]
        read_only_fields = ['date_joined']

    def __init__(self, *args, **kwargs):
        super(ArtisanSerializer, self).__init__(*args, **kwargs)
        request_method = self.context.get('request').method if self.context.get('request') else None

        if request_method == 'POST' or request_method == 'PUT' or request_method == 'PATCH':
            user = UserSerializer() 
            location = serializers.SerializerMethodField()
            service = serializers.SerializerMethodField()
        else:
            # Use SerializerMethodField for read-only fields
            self.fields['location'] = serializers.SerializerMethodField()
            self.fields['service'] = serializers.SerializerMethodField()

    def get_profile_img(self, obj):
        return obj.profile_img.url if obj.profile_img else None

    def get_location(self, obj):
        if obj.location:
            return {
                'id': obj.location.id,
                'location': obj.location.location
            }
        return None

    def get_service(self, obj):
        if obj.service:
            return {
                'id': obj.service.id,
                'title': obj.service.title
            }
        return None
