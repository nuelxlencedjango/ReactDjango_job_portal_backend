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

# Ensure that the list is not empty (for production, this should be explicitly set)
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


SIMPLE_JWT ={
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),

}



#CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS').split(',')



# Application definition

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
    'corsheaders',
    'cloudinary_storage',
    'cloudinary',
    'django_filters',

    #installed app
    'api.apps.ApiConfig',
    'accounts',
    'artisans',
    'transactions',
    'employers',
    'dashboard',
    'services',

   
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
AUTH_USER_MODEL ='accounts.User'
authentication_backend = ['accounts.backends.EmailBackend']


DEFAULT_FILE_STORAGE=os.getenv('DEFAULT_FILE_STORAGE'),
CSRF_TRUSTED_ORIGINS=os.getenv('CSRF_TRUSTED_ORIGINS').split(',')
CORS_ALLOWED_ORIGINS=os.getenv('CORS_ALLOWED_ORIGINS').split(',')
#CORS_ALLOWED_ORIGINS=['https://i-wanwok-backend.up.railway.app,https://react-django-job-portal-frontend-gj7jkwe9f.vercel.app,http://localhost:5173,http://127.0.0.1:8000']
#CSRF_TRUSTED_ORIGINS=['https://i-wanwok-backend.up.railway.app,https://react-django-job-portal-frontend-gj7jkwe9f.vercel.app,http://localhost:5173,http://127.0.0.1:8000']

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
