
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
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
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE)
    artisan = models.ForeignKey('artisans.Artisan', on_delete=models.CASCADE)
    service = models.ForeignKey('api.Service', on_delete=models.CASCADE)
    description = models.TextField()
    address = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    job_date = models.DateField()
    preferred_time = models.TimeField()
    contact_person = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    date_ordered = models.DateTimeField(default=timezone.now, editable=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order by {self.contact_person} for {self.service.title} (Employer: {self.employer.user.username}, Artisan: {self.artisan.user.username})"





class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE)
    service = models.ForeignKey('api.Service', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), 
                                                      ('completed', 'Completed')], 
                                                      default='pending')
    additional_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user 
    