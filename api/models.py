from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.


class Industry(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="The name of the industry")

    def __str__(self):
        return self.name
    


class Service(models.Model):
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=255) 
    time = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=100)
    img = CloudinaryField(blank=True,null=True)

    job_type = models.CharField(max_length=100,null=True, blank=True)
    industry = models.CharField(max_length=100,null=True, blank=True)
    pay_budget = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)


    def __str__(self):
        return self.title




