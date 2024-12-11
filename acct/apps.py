from django.apps import AppConfig


class AcctConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'acct'

    def ready(self):
        import acct.signal # Import the signals when the app is ready



