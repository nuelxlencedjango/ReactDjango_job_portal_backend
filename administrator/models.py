from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.




class Company(models.Model):
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100,null=True, blank=True)
    company_image = CloudinaryField(blank=True,null=True)
    description = models.TextField()
    address = models.CharField(max_length=255)
    date_joined = models.DateField(auto_now_add=True, null=True, blank=True)
    contact = models.CharField(max_length=255) 
    website =  models.CharField(max_length=1000,null=True, blank=True) 
   

    def __str__(self):
        return self.company_name