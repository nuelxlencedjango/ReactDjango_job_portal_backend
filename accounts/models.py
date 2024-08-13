
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

    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.last_name}"

