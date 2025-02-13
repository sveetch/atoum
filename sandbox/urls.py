"""
URL Configuration for sandbox
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("styleguide/", include("sandbox.styleguide.urls", namespace="styleguide")),
    path("", include("atoum.urls")),
]

# This is only needed when using runserver with settings "DEBUG" enabled
if settings.DEBUG:
    try:
        import debug_toolbar  # noqa: F401,F403
    except ImportError:
        pass
    else:
        urlpatterns.append(
            path("__debug__/", include("debug_toolbar.urls"))
        )

    urlpatterns = (
        urlpatterns +
        staticfiles_urlpatterns() +
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
