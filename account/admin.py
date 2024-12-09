
from django.contrib import admin
from .models import CustomUser, ArtisanProfile, EmployerProfile, ManagerProfile
from .models import *




#class UserAdmin(admin.ModelAdmin):
    
 #   list_display = ('username','first_name','last_name','email','artisan','employer','manager','admin')



admin.site.register(CustomUser)


admin.site.register(ArtisanProfile)
admin.site.register(EmployerProfile)
admin.site.register(ManagerProfile)
