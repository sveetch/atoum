"""
Django settings for demonstration

Intended to be used with ``make run``.
"""
from sandbox.settings.base import *  # noqa: F403

DEBUG = True

TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG  # noqa: F405

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": VAR_PATH / "db" / "db.sqlite3",  # noqa: F405
    }
}

# Import local settings if any
try:
    import debug_toolbar  # noqa: F401,F403
except ImportError:
    pass
else:
    INTERNAL_IPS = [
        "192.168.0.115",
    ]

    # # NOTE: Djdt brings some performance issues with some third party libraries like
    # # 'django-import-export' or 'htmx'
    DEBUG_TOOLBAR_PANELS = [
        # "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        # "debug_toolbar.panels.signals.SignalsPanel",
        # "debug_toolbar.panels.redirects.RedirectsPanel",
        # "debug_toolbar.panels.profiling.ProfilingPanel",
    ]

    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE

    # # In provision of possible futur htmx usage
    DEBUG_TOOLBAR_CONFIG = {
        "ROOT_TAG_EXTRA_ATTRS": "hx-preserve"
    }

    INSTALLED_APPS.append("debug_toolbar")

# Import local settings if any
try:
    from .local import *  # noqa: F401,F403
except ImportError:
    pass
