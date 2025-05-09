"""
Django settings for tests
"""
from sandbox.settings.base import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Media directory dedicated to tests to avoid polluting other environment
# media directory
MEDIA_ROOT = VAR_PATH / "media-tests"  # noqa: F405

# All test are written for english language
LANGUAGE_CODE = "en"
# Ensure english language is available
if "en" not in [k for k, v in LANGUAGES]:
    LANGUAGES = LANGUAGES + (("en", "English"),)

# Test environment uses its own Whoosh indexes to not overwrite the ones use in
# sandbox
HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": VAR_PATH / "whoosh_index_tests",
    },
}
