from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin



admin.site.register(Service)
admin.site.register(Industry)


admin.site.register(Area)
admin.site.register(Profession)


