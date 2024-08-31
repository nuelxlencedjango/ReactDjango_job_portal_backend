

from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
import cloudinary
import cloudinary_storage

# Load environment variables from .env file
load_dotenv()

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key for the project
SECRET_KEY = os.getenv('SECRET_KEY')

# Debug mode setting
DEBUG = os.getenv('DEBUG') == 'True'

# Allowed hosts setting
ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS', '').split(',') if host.strip()]
if not ALLOWED_HOSTS:
    raise ValueError("ALLOWED_HOSTS must be set and contain at least one valid hostname.")

# API configurations for Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_COOKIE': 'access_token',
    'AUTH_COOKIE_SECURE': True, 
    'AUTH_COOKIE_HTTP_ONLY': True, 
    'AUTH_COOKIE_PATH': '/',
    'AUTH_COOKIE_SAMESITE': 'Lax',
    'REFRESH_COOKIE_PATH': '/api/token/refresh/',
    'AUTH_COOKIE_DOMAIN': os.getenv('AUTH_COOKIE_DOMAIN'),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}

# Installed apps including rest_framework and rest_framework_simplejwt
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 3rd party libraries
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'cloudinary_storage',
    'cloudinary',
    'django_filters',

    # Installed apps
    'api.apps.ApiConfig',
    'accounts',
    'artisans',
    'transactions',
    'employers',
    'dashboard',
    'services',
]

# Middleware settings including corsheaders middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'icanwork51@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Authentication settings
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = ['accounts.backends.EmailBackend']

# Default file storage
DEFAULT_FILE_STORAGE = os.getenv('DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')

# CORS settings
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if origin.strip()]
CORS_ALLOW_CREDENTIALS = True

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if origin.strip()]

# Enforce HTTPS settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cloudinary configuration
cloudinary.config( 
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET'), 
    secure=os.getenv('SECURE', 'True') == 'True',
)
