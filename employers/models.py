
from django.db import models
from django.contrib.auth.models import User
from artisans.models import *




class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    date_joined = models.DateField(auto_now_add = True, null=True, blank=True)
  
    def __str__(self):
        return f"{self.user.last_name}"
    
    class Meta:
      verbose_name_plural='Employers'
       
      ordering = ['-date_joined']
    


class JobPost(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='job_posts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50, choices=[('full-time', 'Full-Time'), ('part-time', 'Part-Time'), ('contract', 'Contract')])
    industry = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
      verbose_name_plural='JobPosts'
       
      ordering = ['-date_created']
 


class OrderRequest(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_requests')
    artisan = models.ForeignKey('artisans.Artisan', on_delete=models.CASCADE, related_name='received_order')
    request_date = models.DateTimeField(auto_now_add=True)
    #description = models.TextField()
    location = models.CharField(max_length=255)
    service = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order by {self.employer.username} for {self.artisan.user.username}"




class OrderDetails(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_details')
    address = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    description = models.TextField()
    job_date =models.DateTimeField(auto_now_add=True)
    time =models.TimeField(auto_now_add=True)
    contact_person = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    def __str__(self):

        return f"Order Details {self.employer.username} for {self.contact_person}"
    
    