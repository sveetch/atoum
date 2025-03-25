"""
Base Django settings for sandbox
"""

from pathlib import Path

from django import VERSION


SECRET_KEY = "***TOPSECRET***"


# Project paths
BASE_DIR = Path(__file__).parents[2]
PROJECT_PATH = BASE_DIR / "sandbox"
VAR_PATH = BASE_DIR / "var"

DEBUG = False

# Https is never enabled on default and development environment, only for
# integration and production.
HTTPS_ENABLED = False

ADMINS = (
    # ("Admin", "PUT_ADMIN_EMAIL_HERE"),
)

MANAGERS = ADMINS

DATABASES = {}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "Europe/Paris"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "fr"

LANGUAGES = (
    ("en", "English"),
    ('fr', "Français"),
)

# A tuple of directories where Django looks for translation files
LOCALE_PATHS = [
    PROJECT_PATH / "locale",
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# We want to avoid warning for this settings which is deprecated since Django 4.x but
# needed for Django<=3.2
if VERSION[0] < 4:
    # If you set this to False, Django will not format dates, numbers and
    # calendars according to the current locale.
    USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = VAR_PATH / "media"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = VAR_PATH / "static"

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_PATH / "static-sources",
]


MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
]

ROOT_URLCONF = "sandbox.urls"

# Python dotted path to the WSGI application used by Django"s runserver.
WSGI_APPLICATION = "sandbox.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            PROJECT_PATH / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": False,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.forms",
]

# URL to redirect for authentication
LOGIN_URL = "/admin/login/"
# URL to redirect once logged in
LOGIN_REDIRECT_URL = "/"
# URL to redirect once logged out
LOGOUT_REDIRECT_URL = "/"

# Ensure we can override applications widgets templates from project template
# directory, require also 'django.forms' in INSTALLED_APPS
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"


"""
Django smart media configuration using its defaults
"""
from smart_media.settings import *  # noqa: E402,F401,F403

INSTALLED_APPS.extend([
    "sorl.thumbnail",
    "smart_media",
])


"""
django-view-breadcrumbs optional part
"""
try:
    import view_breadcrumbs  # noqa: F401
except ImportError:
    pass
else:
    INSTALLED_APPS[0:0] = [
        "view_breadcrumbs",
    ]


"""
Crispy forms part
"""
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

INSTALLED_APPS.extend([
    "crispy_forms",
    "crispy_bootstrap5",
])


"""
django-autocomplete-light part
"""
INSTALLED_APPS[0:0] = [
    "dal",
    "dal_select2",
]


"""
Styleguide part
"""

INSTALLED_APPS.append("sandbox.styleguide")

# Built CSS manifest relative path to static directory
STYLEGUIDE_MANIFEST_PATH = (
    Path("css") / "components" / "styleguide" / "manifest.css"
)

# JSON manifest dump destination as an absolute path
STYLEGUIDE_DUMP_PATH = (
    PROJECT_PATH / "templates" / "styleguide" / "manifest.json"
)

STYLEGUIDE_SAVE_DUMP = False


"""
django-import-export part
"""

INSTALLED_APPS.append("import_export")

from import_export.formats.base_formats import CSV, HTML, JSON, XLSX, YAML
IMPORT_EXPORT_FORMATS = [CSV, HTML, JSON, XLSX, YAML]


"""
Search engine with django-haystack settings
"""
INSTALLED_APPS.append("haystack")

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": VAR_PATH / "whoosh_index",
    },
}

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20


"""
Atoum settings
"""
from atoum.settings import *  # noqa: E402,F401,F403

INSTALLED_APPS.append("atoum")


"""
Diskette configuration using its defaults
"""
from diskette.settings import *  # noqa: E402,F401,F403

INSTALLED_APPS.append("diskette")

DISKETTE_APPS = [
    [
        "django.contrib.auth", {
            "comments": "django.contrib.auth: user and groups, no perms",
            "natural_foreign": True,
            "models": ["auth.Group","auth.User"]
        }
    ],
    [
        "django.contrib.sites", {
            "comments": "django.contrib.sites",
            "natural_foreign": True,
            "models": "sites"
        }
    ],
    [
        "atoum", {
            "comments": "Atoum",
            "natural_foreign": True,
            "models": "atoum"
        }
    ]
]

DISKETTE_STORAGES = [MEDIA_ROOT]
DISKETTE_STORAGES_EXCLUDES = [
    "cache/*",
    "pil/*",
    "public/thumbnails/*",
]