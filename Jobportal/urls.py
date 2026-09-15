from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#from  accounts.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from acct.views import LoginView
#, CustomTokenObtainPairView, CustomTokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
     path('acct/login/', LoginView.as_view(), name='login'),

   #tokenobtainedpairview
    #path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
   
   path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),  

    path('api/', include('api.urls')),
   
    path('dashboard/', include('dashboard.urls')),
    path('services/', include('services.urls')),
    path('transactions/', include('transactions.urls')),
    path('acct/', include('acct.urls')),
    path('employer/', include('employer.urls')),
    path('administrator/', include('administrator.urls')),
    path('marketers/', include('marketers.urls')),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


