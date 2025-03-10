'''
from django.urls import path
from .views import MarketerDashboardView, RegisterArtisanView

urlpatterns = [
    path('marketer/dashboard/', MarketerDashboardView.as_view(), name='marketer-dashboard'),
    path('marketer/register-artisan/', RegisterArtisanView.as_view(), name='register-artisan'),
]
'''