
from django.db import models

from cloudinary.models import CloudinaryField
from accounts.models import *
from services.models import *
from accounts.models import User
from api.models import *

from django.db.models.signals import post_save
from django.dispatch import receiver


LAGOS_ZONES =(
    ('Alimosho' ,'Alimosho'),
    ('Ajeromi-Ifelodun' ,'Ajeromi-Ifelodun'),
    ('Kosofe' ,'Kosofe'),
    ('Mushin' ,'Mushin'),
    ('Oshodi-Isolo' ,'Oshodi-Isolo'),
    ('Ojo' ,'Ojo'),
    ('Ikorodu' ,'Ikorodu'),
    ('Surulere' ,'Surulere'),
    ('Agege' ,'Agege'),
    ('Ifako-Ijaiye' ,'Ifako-Ijaiye'),
    ('Somolu' ,'Somolu'),
    ('Amuwo-Odofin' ,'Amuwo-Odofin'),

    ('Lagos Mainland' ,'Lagos Mainland'),
    ('Ikeja' ,'Ikeja'),
     ('Eti-Osa' ,'Eti-Osa'),
    ('Badagry' ,'Badagry'),
    ('Apapa' ,'Apapa'), 
    ('Lagos Island' ,'Lagos Island'),
    ('Epe' ,'Epe'), 
    ('Ibeju-Lekki' ,'Ibeju-Lekki'), 
    ('Ikoyi-obalende' ,'Ikoyi-obalende'),

)
# Create your models here.

class Area(models.Model):
   area_code = models.CharField(max_length=3)
   location = models.CharField(max_length=100,unique=True)
    
   def __str__(self):
      return self.location
   
   class Meta:
      verbose_name_plural = "Area"
      

class Profession(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name




class Artisan(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='artisan_profile')
    nin = models.CharField(max_length=11, unique=True)
    location = models.ForeignKey('Area', on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey('api.Service', related_name='artisans', on_delete=models.CASCADE, null=True, blank=True)
    experience = models.IntegerField(help_text="Experience in years")
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    profile_img = CloudinaryField(blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True, null=True, blank=True)

    job_type = models.CharField(max_length=100, null=True, blank=True)
    industry =  models.ForeignKey('api.Industry',related_name='industry_type',on_delete=models.CASCADE, null=True, blank=True)
    pay = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)

    class Meta:
      verbose_name_plural='Artisans'
      ordering = ['-date_joined']

    def __str__(self):
        if self.user:
            return f"{self.user.last_name}- {self.service}"
        return f"Artisan {self.id} - {self.service}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_artisan:
        Artisan.objects.create(user=instance)

