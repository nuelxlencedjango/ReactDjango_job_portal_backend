from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin



#admin.site.register(Employer)
#admin.site.register(JobPost)
#admin.site.register(Cart)
#admin.site.register(CartItem)

'''
class OrderRequestAdmin(admin.ModelAdmin):
    
    list_display = ('employer','artisan','service','description','address',
                    'area','job_date','preferred_time','contact_person',
                    'phone_number','date_ordered','paid')

class OrderAdmin(admin.ModelAdmin):
    list_display = ['employer','phone_number','data_ordered']

admin.site.register(OrderRequest,OrderRequestAdmin)

'''