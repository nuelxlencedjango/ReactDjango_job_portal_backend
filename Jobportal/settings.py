"""
Django settings for Jobportal project. 

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
#3rd party imports
import dj_database_url
from datetime import timedelta
from dotenv import load_dotenv
from decouple import config
#cloudnary lib
import cloudinary
import cloudinary.uploader
import cloudinary.api
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=os.getenv('SECRET_KEY') 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=os.getenv('DEBUG') 

# SECURITY WARNING: keep the secret key used in production secret!


# Get ALLOWED_HOSTS from environment variable, default to empty list if not set

allowed_hosts_env = os.getenv('ALLOWED_HOSTS','')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',') if host.strip()]
if not ALLOWED_HOSTS:
    raise ValueError("ALLOWED_HOSTS must be set and contain at least one valid hostname.")



#API Configurations

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Secret key and other settings...



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_COOKIE': 'access_token',
    'AUTH_COOKIE_SECURE': True,  # Set to True for HTTPS (use in production)
    'AUTH_COOKIE_HTTP_ONLY': True,  # To prevent access to the cookie via JavaScript
    'AUTH_COOKIE_PATH': '/',  # Cookie will be sent with every request
    'AUTH_COOKIE_SAMESITE': 'None',  # Set to 'None' to allow cross-origin cookies
    'REFRESH_COOKIE_PATH': '/api/token/refresh/',
    #'AUTH_COOKIE_DOMAIN': os.getenv('AUTH_COOKIE_DOMAIN', '.example.com'),  # Update with your domain
    #'AUTH_COOKIE_DOMAIN': os.getenv('AUTH_COOKIE_DOMAIN', '.example.com'),
    'AUTH_COOKIE_DOMAIN': os.getenv('AUTH_COOKIE_DOMAIN', '.vercel.app'),  # Allow cookies to be shared across all subdomains under vercel.app

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}

CSRF_COOKIE_SAMESITE = 'None'  # Allows CSRF cookie to be sent with cross-origin requests
SESSION_COOKIE_SAMESITE = 'None'  # Allows session cookie to be sent with cross-origin requests

CSRF_COOKIE_SECURE = True  # Ensure CSRF cookie is only sent over HTTPS in production
SESSION_COOKIE_SECURE = True  # Ensure session cookie is only sent over HTTPS in production
SameSite=None



# settings.py

FRONTEND_URL = 'https://react-django-job-portal-frontend.vercel.app' 



#CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

     #3rd party libraries
    'rest_framework',
   # 'rest_framework.authtoken',
    'corsheaders',
    'cloudinary_storage',
    'cloudinary',
    'django_filters',

    #installed app
    'api.apps.ApiConfig',
    'acct.apps.AcctConfig',
    #'accounts',
   # 'artisans',
    'transactions',
    #'employers',
    'dashboard',
    'services',
    'social_account',
    'employer',
    'administrator',

   
]




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
     'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #corsheaders middleware
    'corsheaders.middleware.CorsMiddleware',
    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


ROOT_URLCONF = 'Jobportal.urls' 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Jobportal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
      'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE'), 
        'NAME': os.getenv('DATABASE_NAME'),
        'HOST' :os.getenv('DATABASE_HOST'),
        'PORT':os.getenv('DATABASE_PORT'),
        'USER' :os.getenv('DATABASE_USER'),
        'PASSWORD' :os.getenv('DATABASE_PASSWORD'),

    }
}




# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



cloudinary.config( 
  cloud_name=os.getenv('CLOUD_NAME'),
  api_key=os.getenv('API_KEY'), 
  api_secret=os.getenv('API_SECRET'), 
  secure=os.getenv('SECURE'),
 
)


#authentication
AUTH_USER_MODEL ='acct.CustomUser'
authentication_backend = ['accounts.backends.EmailBackend']


DEFAULT_FILE_STORAGE=os.getenv('DEFAULT_FILE_STORAGE')
#CSRF_TRUSTED_ORIGINS=os.getenv('CSRF_TRUSTED_ORIGINS','').split(',')
CORS_ALLOWED_ORIGINS=os.getenv('CORS_ALLOWED_ORIGINS','').split(',')


CORS_ALLOW_CREDENTIALS = True

# Enforce HTTPS
SECURE_SSL_REDIRECT = True

# If behind a proxy like Vercel or Railway, add this:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


   #EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER ='icanwork51@gmail.com'
EMAIL_HOST_PASSWORD  = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'



# Define CSRF trusted origins
csrf_trusted_origins_env = os.getenv('CSRF_TRUSTED_ORIGINS', '')
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_trusted_origins_env.split(',') if origin.strip()]

if not CSRF_TRUSTED_ORIGINS:
    raise ValueError("CSRF_TRUSTED_ORIGINS must be set and contain at least one valid origin.")

# Example of trusted origins configuration:
# CSRF_TRUSTED_ORIGINS = ['https://react-django-job-portal-frontend.vercel.app', 'http://localhost:5173']


#FLUTTERWAVE_PUBLIC_KEY = os.getenv('FLUTTERWAVE_PUBLIC_KEY').strip()
#FLUTTERWAVE_SECRET_KEY = os.getenv('FLUTTERWAVE_SECRET_KEY').strip()
FLUTTERWAVE_SECRET_KEY=config('FLUTTERWAVE_SECRET_KEY')
# settings.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',  # Log INFO level and above
            'class': 'logging.FileHandler',
            'filename': 'debug.log',  # Log file path
        },
        'console': {
            'level': 'INFO',  # Log INFO level and above
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}