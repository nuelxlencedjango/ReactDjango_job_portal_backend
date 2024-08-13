
from django.contrib import admin
from accounts.models import *




class UserAdmin(admin.ModelAdmin):
    
    list_display = ('username','first_name','last_name','email','is_artisan','is_employer','is_manager','is_admin')



admin.site.register(User,UserAdmin)
