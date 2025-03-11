
from django.urls import path
from .views import MarketerRegistrationView

urlpatterns = [
    path('marketer-register/', MarketerRegistrationView.as_view(), name='marketer-register'),
    #  path('marketer/dashboard/', MarketerDashboardView.as_view(), name='marketer-dashboard'),
]