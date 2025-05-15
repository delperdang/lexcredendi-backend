import os
from pathlib import Path
from import_export.formats.base_formats import CSV

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in (
    "true",
    "1",
    "t",
    "on",
    "yes",
)

ALLOWED_HOSTS = [
    "delperdang.pythonanywhere.com",
    "https://delperdang.github.io",
    "http://localhost",
    "http://127.0.0.1",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "tz_detect",
    "import_export",
    "home.apps.HomeConfig",
    "apologetics.apps.ApologeticsConfig",
    "art.apps.ArtConfig",
    "bible.apps.BibleConfig",
    "catechism.apps.CatechismConfig",
    "doctrine.apps.DoctrineConfig",
    "litcal.apps.LitcalConfig",
    "prayer.apps.PrayerConfig",
    "readings.apps.ReadingsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "tz_detect.middleware.TimezoneMiddleware",
]

ROOT_URLCONF = "lexcredendi.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "lexcredendi.context_processors.environ_vars",
            ],
        },
    },
]

WSGI_APPLICATION = "lexcredendi.wsgi.application"
ASGI_APPLICATION = "lexcredendi.asgi.application"

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "lexcredendi_db",
        "USER": "delperdang",
        "PASSWORD": DB_PASSWORD,
        "HOST": "delperdang.mysql.pythonanywhere-services.com",
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        },
    }
}

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = "/home/delperdang/lexcredendi/static"
MEDIA_URL = "/media/"
MEDIA_ROOT = "/home/delperdang/lexcredendi/media"

if DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    STATIC_ROOT = os.path.join(BASE_DIR, "static")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOWED_ORIGINS = [
    "https://delperdang.github.io",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

CORS_ALLOW_CREDENTIALS = True

TZ_DETECT_COUNTRIES = ("US", "CA", "GB", "AU")

IMPORT_EXPORT_FORMATS = [CSV]

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
