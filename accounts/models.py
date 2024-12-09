
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


    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['username']

   

'''



'''













# 1st modeel
# models.py


#1st model end


#2nd model


#end 2nd model





'''

# Custom User Model
class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employer', 'Employer'),
        ('artisan', 'Artisan'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    date_joined = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

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


# Abstract Base Profile
class BaseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    location = models.ForeignKey('api.Area', on_delete=models.CASCADE, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.username} Profile"


# Artisan Profile
class ArtisanProfile(BaseProfile):
    service = models.ForeignKey('api.Service', related_name='artisans', on_delete=models.CASCADE, null=True, blank=True)
    experience = models.PositiveIntegerField(null=True, blank=True)
    fingerprint_image = CloudinaryField('fingerprints', null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_image = CloudinaryField('profile_images', null=True, blank=True)
    nin = models.CharField(max_length=11, unique=True)
    job_type = models.CharField(max_length=50, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    pay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


# Employer Profile
class EmployerProfile(BaseProfile):
    company_name = models.CharField(max_length=255, null=True, blank=True)


# Manager Profile
class ManagerProfile(BaseProfile):
    department = models.CharField(max_length=100, null=True, blank=True)

'''







