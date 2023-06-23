import os
from decouple import config
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'templates', 'sw.js')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# remember on same level as manage.py
SECRET_KEY = config('SECRET_KEY')
OPENAI_SECRET_KEY = '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'
# OPENAI_SECRET_KEY = config('OPENAI_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)
USE_S3 = config('USE_S3', cast=bool)


ALLOWED_HOSTS = ['*']
LOGIN_URL = "/login"
MAX_SKIT_LENGTH = 240
SKIT_ACTION_OPTIONS = ["like", "dislike", "repost"]
URL = "//skitte.co"
INTERNAL_IPS = ('127.0.0.1', 'localhost',
                'www.skitte.co', 'skitte.co')
                
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    'django_cleanup.apps.CleanupConfig',
    'corsheaders',
    'channels',
    'rest_auth',
    'rest_auth.registration',
    'rest_framework',
    'rest_framework.authtoken',
    'debug_toolbar',
    'storages',

    'pwa',

    # GraphQL
    'graphene_django',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',  # refresh tokens are optional
    "graphql_auth",

    # my app
    'skit',
    # 'skitte_chat',
    'accounts',
    'profiles',
    'expo',
]

AUTH_USER_MODEL = 'accounts.User'
CONTACT_MODEL = 'profiles.Profile'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
LOGIN_REDIRECT_URL = '/feed'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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

# Channels
WSGI_APPLICATION = 'skitte.wsgi.application'
ASGI_APPLICATION = "skitte.asgi.application"


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}


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


# STMP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# For React
CORS_ORIGIN_ALLOW_ALL = True  # any website has access to my api
CORS_URLS_REGEX = r'^/api/.*$'
CSRF_COOKIE_NAME = "csrftoken"
DEFAULT_RENDERER_CLASSES = [
    'rest_framework.renderers.JSONRenderer',
]

DEFAULT_AUTHENTICATION_CLASSES = [
    'rest_framework.authentication.SessionAuthentication',
]

if DEBUG:
    DEFAULT_RENDERER_CLASSES += [
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
    DEFAULT_AUTHENTICATION_CLASSES += [
        'skitte.rest_api.dev.DevAuthentication'
    ]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': DEFAULT_AUTHENTICATION_CLASSES,
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES
}


AUTHENTICATION_BACKENDS = [
    "graphql_auth.backends.GraphQLAuthBackend",
    'django.contrib.auth.backends.ModelBackend',
]

GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,

    # optional
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,

    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
        "graphql_auth.mutations.ResendActivationEmail",
        "graphql_auth.mutations.SendPasswordResetEmail",
        "graphql_auth.mutations.PasswordReset",
        "graphql_auth.mutations.ObtainJSONWebToken",
        "graphql_auth.mutations.VerifyToken",
        "graphql_auth.mutations.RefreshToken",
        "graphql_auth.mutations.RevokeToken",
        "graphql_auth.mutations.VerifySecondaryEmail",
    ],
}

GRAPHENE = {
    'SCHEMA': 'skit.graphql.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}
GRAPHQL_AUTH = {
    'SEND_ACTIVATION_EMAIL': True,
    "REGISTER_MUTATION_FIELDS": [
        'first_name', 'last_name', 'username', 'email', 'password1', 'password2']
}

PWA_APP_NAME = 'Skitte'
PWA_APP_DESCRIPTION = "Skitte A Trusted Social Media Network Were A Comfortable Community Network Is Developed."
PWA_APP_THEME_COLOR = '#4CAF50'
PWA_APP_BACKGROUND_COLOR = '#0C0C0C'
PWA_APP_DISPLAY = 'minimal-ui'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'portrait'
PWA_APP_START_URL = '/feed'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        "src": f"{STATIC_URL}media/logo/icon-256x256.png",
        "sizes": "256x256",
        "type": "image/png"
    },
    {
        "src": f"{STATIC_URL}media/logo/1024.png",
        "sizes": "1024x1024",
        "type": "image/png"
    },
    {
        "src": f"{STATIC_URL}media/logo/icon-512x512.png",
        "sizes": "512x512",
        "type": "image/png"
    },
    {
        "src": f"{STATIC_URL}media/skitte-logo-curve-rectangle.png",
        "sizes": "341x222",
        "type": "image/png"
    },
]
PWA_APP_ICONS_APPLE = [
    {
        "src": f"{STATIC_URL}media/logo/icon-192x192.png",
        "sizes": "192x192",
        "type": "image/png"
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': f'{STATIC_URL}media/skitte-logo-curve-rectangle.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
