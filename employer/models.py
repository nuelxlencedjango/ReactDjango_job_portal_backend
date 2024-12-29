from django.db import models
#from django.contrib.auth.models import User
from django.utils import timezone
from acct.models import CustomUser, ArtisanProfile, EmployerProfile
from django.conf import settings
import random
import string
import uuid
# Create your models here.






class Cart(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    cart_code = models.CharField(max_length=11, unique=True, editable=False)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.cart_code:
            self.cart_code = self.generate_cart_code()
        super().save(*args, **kwargs)

    def generate_cart_code(self):
        """Generates a unique 11-character alphanumeric cart code."""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=11))
            if not Cart.objects.filter(cart_code=code).exists():
                return code

    def __str__(self):
        return f"Cart {self.cart_code} for {self.user.last_name}"
    



class CartItem(models.Model):
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    artisan = models.ForeignKey('acct.ArtisanProfile', on_delete=models.CASCADE)
    service = models.ForeignKey('api.Service', on_delete=models.CASCADE)
    unique_reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    #price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 

    def __str__(self):
        return f"{self.quantity} x {self.service.title} (Artisan: {self.artisan.user.username}, Employer: {self.employer.last_name})"





class Checkout(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    amount = models.CharField(max_length=15,null=True, blank=True)
    unique_reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    #shipping_address = models.TextField()
   # billing_address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    


class JobDetails(models.Model):
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,blank=True)
    description = models.TextField()
    artisan = models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    contact_person_phone = models.CharField(max_length=15)
    expectedDate = models.DateTimeField(auto_now_add=True)
    #added_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f" Employer: {self.employer.last_name} x  (Artisan: {self.artisan.user.first_name})"

