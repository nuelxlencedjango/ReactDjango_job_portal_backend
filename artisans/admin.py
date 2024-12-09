from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin




class ArtisansAdmin(admin.ModelAdmin):
    
    list_display = ['user','service','nin','location','address','experience','phone','date_joined','id']


class AreaAdmin(admin.ModelAdmin):
    list_display = ['location','area_code']


#admin.site.register(Artisan,ArtisansAdmin)
#admin.site.register(Area,AreaAdmin)
#admin.site.register(Profession)

