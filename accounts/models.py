
from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    first_name =models.CharField(max_length=20,blank=True, null=True)
    last_name =models.CharField(max_length=20,blank=True, null=True)
    email = models.EmailField(unique=True)
    is_artisan = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.last_name}"
"""
"""

    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['username']

   


'''
from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

# Custom User Model with user type
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employer', 'Employer'),
        ('artisan', 'Artisan'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    
    # Additional fields common to all user types
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    def is_admin(self):
        return self.user_type == 'admin'

    def is_manager(self):
        return self.user_type == 'manager'

    def is_employer(self):
        return self.user_type == 'employer'

    def is_artisan(self):
        return self.user_type == 'artisan'


# Profession Model (if needed for Artisan)
class Profession(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


# User Profile Base Model (for Artisan, Employer, Manager, etc.)
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    # Common fields for all user types
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True  # Ensure it's not used directly

    def __str__(self):
        return f"{self.user.username}'s profile"


# Artisan Profile
class ArtisanProfile(UserProfile):
    profession = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    fingerprint_image = CloudinaryField('fingerprints', null=True, blank=True)
    live_face_capture = CloudinaryField('face_captures', null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} - Artisan Profile'


# Employer Profile
class EmployerProfile(UserProfile):
    company_name = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.user.username} - Employer Profile'


# Manager Profile
class ManagerProfile(UserProfile):
    def __str__(self):
        return f'{self.user.username} - Manager Profile'


# User registration signal to create the profile automatically (optional)
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'artisan':
            ArtisanProfile.objects.create(user=instance)
        elif instance.user_type == 'employer':
            EmployerProfile.objects.create(user=instance)
        elif instance.user_type == 'manager':
            ManagerProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_artisan():
        instance.artisanprofile.save()
    elif instance.is_employer():
        instance.employerprofile.save()
    elif instance.is_manager():
        instance.managerprofile.save()
'''