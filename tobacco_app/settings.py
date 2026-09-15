"""
Django settings for tobacco_app project.
"""

import os
from pathlib import Path
#import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-sw_l0sr!z$rb2p*c3^n-k#9*=%v8y-_i8tx^_)2h^!!@-)#w-l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

'''
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


#.env cong (django-environ)
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')
'''
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'classifier',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    ##'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tobacco_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'tobacco_app.wsgi.application'

#temp
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

'''
# Database — set DATABASE_URL for PostgreSQL (etc.); otherwise local SQLite.
if os.environ.get("DATABASE_URL"):
    DATABASES = {
        #"default": dj_database_url.config(conn_max_age=600),
        "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        },
    }
'''

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Compressed/cached static assets (used with collectstatic + Gunicorn)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media files (Uploaded images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Model files directories
MODEL_ROOT = os.path.join(BASE_DIR, 'models')
TOBACCO_DETECTOR_MODEL = os.path.join(MODEL_ROOT, 'tobacco_detector.h5')
CLASSIFIER_MODEL = os.path.join(MODEL_ROOT, '2classifier_model.h5')
LABEL_BINARIZER = os.path.join(MODEL_ROOT, '2label_binarizer.pkl')
PRICING_MODEL = os.path.join(MODEL_ROOT, 'nn_pricing.h5')
ENCODER_FILE = os.path.join(MODEL_ROOT, 'nn_encoder.npy')

# Authentication settings
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
'''
#  Oracle Cloud Object Storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = env('OCI_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = env('OCI_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = env('OCI_BUCKET_NAME')
AWS_S3_REGION_NAME = env('OCI_REGION')

# Oracle S3-compatible endpoint
AWS_S3_ENDPOINT_URL = f"https://{env('OCI_NAMESPACE')}.compat.objectstorage.{env('OCI_REGION')}.oraclecloud.com"

AWS_S3_FILE_OVERWRITE = False        # don't overwrite files with same name
AWS_DEFAULT_ACL = 'public-read'      # files publicly accessible
AWS_QUERYSTRING_AUTH = False         # clean URLs without auth tokens

# Media files now served from Oracle Cloud
MEDIA_URL = f"https://{env('OCI_NAMESPACE')}.compat.objectstorage.{env('OCI_REGION')}.oraclecloud.com/{env('OCI_BUCKET_NAME')}/"
'''
