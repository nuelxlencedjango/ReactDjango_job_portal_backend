from django.contrib import admin
from .models import CustomUser, ArtisanProfile, EmployerProfile, ManagerProfile,BaseProfile
#from accounts.models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    
    list_display = ('username','first_name','last_name','email','artisan','employer','manager','admin','date_joined')



admin.site.register(CustomUser)
#admin.site.register(BaseProfile)

admin.site.register(ArtisanProfile)
admin.site.register(EmployerProfile)
admin.site.register(ManagerProfile)