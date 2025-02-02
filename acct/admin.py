from django.contrib import admin
from .models import (CustomUser, ArtisanProfile, EmployerProfile, 
                    Fingerprint, ManagerProfile)
from django.contrib.auth.admin import UserAdmin




class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(ArtisanProfile)
admin.site.register(EmployerProfile)
admin.site.register(ManagerProfile)
admin.site.register(Fingerprint)


