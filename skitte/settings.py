import os
import dj_database_url
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def config(var, default=None):
    try:
        return os.environ[var]
    except KeyError:
        if default is not None:
            return default
        error_msg = f"Set the {var} environment variable"
        raise Exception(error_msg)

SECRET_KEY = config('SECRET_KEY', 'secret-key')
OPENAI_SECRET_KEY = config('OPENAI_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', True)
USE_S3 = config('USE_S3', False)


ALLOWED_HOSTS = ['*']
LOGIN_URL = "/login"
URL = "//expo.skitte.co"
INTERNAL_IPS = ('127.0.0.1', 'localhost',
                'expo.skitte.co')
                
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
    'storages',
    'expo',
]
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skitte.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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


WSGI_APPLICATION = 'skitte.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'skitte.sqlite3'),
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'skitte_db_test.sqlite3')
        }
    }
}
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

COMPRESS_ENABLED = True
COMPRESS_CSS_HASHING_METHOD = 'content'
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = config('AWS_DEFAULT_ACL')
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.eu-west-2.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_S3_SECURE_URLS = True
    # storage
    # DEFAULT_FILE_STORAGE = 'skitte.storage_backends.CachedStaticS3BotoStorage'
    # STATICFILES_STORAGE = 'skitte.storage_backends.MediaS3BotoStorage'

    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'skitte.storage_backends.StaticStorage'
    COMPRESS_URL = STATIC_URL
    COMPRESS_ROOT = BASE_DIR + "/static-root/"
    COMPRESS_STORAGE = 'skitte.storage_backends.CachedStaticS3BotoStorage'

    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'sktmedia'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'skitte.storage_backends.PublicMediaStorage'
    # MEDIA_ROOT = PUBLIC_MEDIA_LOCATION

    # CORS_ORIGIN_WHITELIST = ("https://www.skitte.co",
    #  f"https://{AWS_S3_CUSTOM_DOMAIN}", "https://skitte.herokuapp.com")

elif not USE_S3:
    STATIC_URL = '/static/'
    MEDIA_URL = '/sktmedia/'
    STATIC_ROOT = os.path.join(BASE_DIR, "static-root")
    MEDIA_ROOT = os.path.join(BASE_DIR, "sktmedia")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]