from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin



admin.site.register(Employer)
admin.site.register(JobPost)
admin.site.register(OrderRequest)
admin.site.register(OrderDetails)