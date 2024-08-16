
"""
URL configuration for Jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#from api.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from  accounts.views import * #RegisterView, LoginView
from django.views.generic import TemplateView
from django.urls import path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
     path('accounts/login/', LoginView.as_view(), name='login'),

   #tokenobtainedpairview
    path('api/token/', TokenObtainPairView.as_view(), name='get_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api-auth/', include('rest_framework.urls')),  

    # Catch-all route for React
     #re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),



    path('', include('api.urls')),
    path('artisans/', include('artisans.urls')),
    path('accounts/', include('accounts.urls')),
    path('employers/', include('employers.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('services/', include('services.urls')),
    path('transactions/', include('transactions.urls')),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

