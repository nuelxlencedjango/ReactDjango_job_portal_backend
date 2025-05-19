
from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from PIL import Image
from io import BytesIO
import requests
from django.core.files.base import ContentFile
from decimal import Decimal
import cloudinary
import cloudinary.uploader
import cloudinary.api



import logging
logger = logging.getLogger(__name__)



# Custom User Model
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employer', 'Employer'),
        ('artisan', 'Artisan'),
        ('marketer', 'Marketer'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    date_joined = models.DateField(auto_now_add=True, null=True, blank=True)


    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ('username','username')
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} - ({self.get_user_type_display()})"

    @property
    def is_admin(self):
        return self.user_type == 'admin'

    @property
    def is_manager(self):
        return self.user_type == 'manager' 

    @property
    def is_employer(self):
        return self.user_type == 'employer'

    @property
    def is_artisan(self):
        return self.user_type == 'artisan'
    
    @property
    def is_marketer(self):
        return self.user_type == 'marketer'
    
    


# Abstract Base Profile
class BaseProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True, unique=True) 
    location = models.ForeignKey('api.Area', on_delete=models.CASCADE, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.username} Profile"


# Maketer Profile
class MarketerProfile(BaseProfile):
    address = models.CharField(max_length=500, null=True, blank=True)
    profile_image = CloudinaryField(null=True, blank=True)
    
    def __str__(self):
        return f"Marketer: {self.user.first_name} {self.user.last_name}"
    
    



from cloudinary.uploader import upload




class ArtisanProfile(BaseProfile):
    service = models.ForeignKey('api.Service', related_name='artisans', on_delete=models.CASCADE, null=True, blank=True)
    experience = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_image = CloudinaryField(null=True, blank=True)
    #profile_image_resized = models.ImageField(upload_to='profile_images/resized/', null=True, blank=True)
    nin = models.CharField(max_length=11, unique=True, null=True, blank=True)
    job_type = models.CharField(max_length=50, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    pay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    marketer = models.ForeignKey(MarketerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='registered_artisans')
    
    def save(self, *args, **kwargs):
        """Override the save method to handle image resizing and optimization."""

        if not self.pk or 'commission' not in self.__dict__:  # Only for new records
            if self.pay:
                self.commission = round(self.pay * Decimal('0.10'), 2)
               
                self.pay = self.pay + self.commission
        

        if self.profile_image and not self.pk:  # Only process new images
            try:
                # Upload the image to Cloudinary with resizing and optimization
                result = upload(self.profile_image,
                    transformation=[{"width": 800, "height": 800, "crop": "limit"}  # Resize to max 800x800
                ],
                    quality="auto",  # Optimize image quality
                    fetch_format="auto"  # Automatically choose the best format (e.g., webp)
                )
                # Update the profile_image field with the Cloudinary public_id
                self.profile_image = result['public_id']
            except Exception as e:
                # Log the error and continue without resizing
                print(f"Failed to upload image to Cloudinary: {str(e)}")
        
        super().save(*args, **kwargs)
    





# Employer Profile
class EmployerProfile(BaseProfile):
    
    company_name = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# Manager Profile
class ManagerProfile(BaseProfile):
    department = models.CharField(max_length=100, null=True, blank=True)
    profile_image = CloudinaryField(null=True, blank=True)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"







class Fingerprint(models.Model): 
    artisan_profile = models.ForeignKey('ArtisanProfile', related_name='fingerprints', on_delete=models.CASCADE)

    fingerprint_image = CloudinaryField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fingerprint for {self.artisan_profile.user.first_name} {self.artisan_profile.user.last_name} at {self.created_at}"

    class Meta:
        ordering = ['-created_at']








