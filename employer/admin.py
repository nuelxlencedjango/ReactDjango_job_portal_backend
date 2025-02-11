from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin



admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Checkout)
admin.site.register(JobDetails)
admin.site.register(PaymentInformation)



