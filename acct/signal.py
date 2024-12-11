
# signal.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, ArtisanProfile, EmployerProfile, ManagerProfile

# Signal to Automatically Create Profiles
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'artisan':
            ArtisanProfile.objects.create(user=instance)
        elif instance.user_type == 'employer':
            EmployerProfile.objects.create(user=instance)
        elif instance.user_type == 'manager':
            ManagerProfile.objects.create(user=instance)

# Signal to Automatically Save Profiles
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'artisanprofile'):
        instance.artisanprofile.save()
    elif hasattr(instance, 'employerprofile'):
        instance.employerprofile.save()
    elif hasattr(instance, 'managerprofile'):
        instance.managerprofile.save()




