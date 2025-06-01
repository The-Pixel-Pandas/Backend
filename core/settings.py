# settings.py

from pathlib import Path
import os
# No longer importing dj_database_url if you're fully switching
from dotenv import load_dotenv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file (for local development)
# Ensure you have a .env file in your project root for local development
# and add it to .gitignore
# This .env file should now contain POSTGRESQL_DB_... variables for local use
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    print(f"Warning: .env file not found at {env_path}. Environment variables should be set externally.")


# SECURITY WARNING: keep the secret key used in production secret!
# Get SECRET_KEY from environment variable
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-v(rq1ogk007#2axhaoa(hri6u%kl1b^v_hrhsn8#ib$q_=1e#q')

# SECURITY WARNING: don't run with debug turned on in production!
# Get DEBUG status from environment variable (True by default for local dev, False for production)
# Default to 'False' if DEBUG is not explicitly set, which is safer for production.
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Get allowed hosts from environment variable
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,pixel-pandas.liara.run').split(',')
# If DEBUG is False and you have other production domains, add them.
# For Liara, your specific app URL is the most important one here.
# You might also consider getting this from an environment variable in production if it changes.
# Example: ALLOWED_HOSTS_PROD = os.environ.get('ALLOWED_HOSTS_PROD')
# if ALLOWED_HOSTS_PROD:
#     ALLOWED_HOSTS.extend(ALLOWED_HOSTS_PROD.split(','))


AUTH_USER_MODEL = 'accounts.User' # From your previous settings

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic", # For serving static files efficiently
    "django.contrib.staticfiles",
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'accounts', # Your app from previous settings
    'corsheaders',
    'postgresql_app',
]

REST_FRAMEWORK = { # From your previous settings
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

from datetime import timedelta # From your previous settings
SIMPLE_JWT = { # From your previous settings
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY, # Uses the SECRET_KEY defined above
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", # WhiteNoise middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls" # Assuming 'core' is your project name

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'], # Good practice for project-level templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application" # Assuming 'core' is your project name


# Database
# Configuration according to the Liara tutorial (individual environment variables)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'root',
        'PASSWORD': '8PWotfbYpvc5BOgmQzrlfnBm',
        'HOST': 'tahlil',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'sslmode': 'require'
        }
    }
}

# Optional: Add SSL mode for PostgreSQL if required by Liara and not handled by the host string
# This is often needed for managed cloud databases. Check Liara's recommendations.
# if os.getenv("POSTGRESQL_DB_HOST") and not DEBUG: # Example: enable SSL in production
#     DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles" # Directory where collectstatic will gather them
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files (User-uploaded files) - Liara might have specific recommendations for this
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles' # Ensure this directory exists or is created


# Default primary key field type
# https://docs.djangoproject.com/en/dev/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# CORS settings from your previous configuration
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173,https://pixel-pandas.liara.run').split(',')
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173,https://pixel-pandas.liara.run').split(',')

# Security settings for production (use environment variables to control these)
# These should be True in production (when DEBUG=False)
# Defaulting to False if the env var is not set, but will be True if DEBUG is False
# and the env var is not explicitly 'False'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', str(not DEBUG)).lower() == 'true'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', str(not DEBUG)).lower() == 'true'

# Optional additional security settings for production (when DEBUG=False)
# SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', str(not DEBUG)).lower() == 'true'
# SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 0 if DEBUG else 31536000)) # e.g., 1 year for prod
# SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', str(not DEBUG)).lower() == 'true'
# SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', str(not DEBUG)).lower() == 'true'
# SECURE_BROWSER_XSS_FILTER = True # Good to have
# SECURE_CONTENT_TYPE_NOSNIFF = True # Good to have

# CSRF settings from your previous configuration
CSRF_COOKIE_SAMESITE = 'Lax'
# CSRF_COOKIE_HTTPONLY default is False, which is usually fine.
# If your JavaScript does not need to read the CSRF token from the cookie, you can set it to True.
# CSRF_COOKIE_HTTPONLY = True