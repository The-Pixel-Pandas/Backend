from .settings import *  # Import all settings from the main settings file

# Override the DATABASES setting to use SQLite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # SQLite database file
    }
}

# Debug mode for local development
DEBUG = True

# Allowed hosts for local development
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# CORS settings for local development
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]