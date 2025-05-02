import base64

from django.conf import settings
from django.contrib.sites.models import Site

from atoum import __version__


def get_project_globals(with_siteobject=False, with_static=False, with_media=False,
                        is_secure=False, extra={}):
    """
    Return global informations from project and the current Site object.

    This can be used in code out of a Django requests (like in management
    commands) or in a context processor to get the Site url.

    Return globals (typed as they would be used from a template):

    SITE.name
        Current *Site* entry name.
    SITE.domain
        Current *Site* entry domain.
    SITE.web_url
        The Current *Site* entry domain prefixed with the http protocol like
        ``http://mydomain.com``. If HTTPS is enabled 'https' will be used instead of
        'http'.
    SITE.scheme
        Either return ``https`` or ``http`` depending ``is_secure`` argument is true
        or not.
    PROJECT.release
        Current project release version.
    PROJECT.release_base64
        Current project release version encoded in base64.

    ``SITE`` part depends from ``with_siteobject`` argument.

    It can have also ``STATIC_URL`` and ``MEDIA_URL`` variable if enabled from
    arguments.

    And optionally there can be extra variables from setting ``EXTRA_PROJECT_GLOBALS``,
    its content will be available in 'EXTRA' context variable.

    .. Warning:
        Don't add any secret variable here since it is widely exposed and may even
        be displayed from view ``ExposedSiteMetasView``. This would be a major security
        breach.

    Keyword Arguments:
        with_siteobject (boolean): If True adds ``SITE`` part to returned dict. Default
            is False.
        with_static (boolean): If True adds ``STATIC_URL`` to returned dict. Default
            is False.
        with_media (boolean): If True adds ``MEDIA_URL`` to returned dict. Default
            is False.
        is_secure (boolean): If True the site url will be in ``https``. Default
            is False.
        extra (dict): Additional variables to add. This update the whole main data
            dictionnary so you should not use ``SITE``, ``PROJECT`` item names else it
            would lost their original content. This is another possibility to add extra
            data in addition to the ``EXTRA`` part.

    Returns:
        dict: Meta informations.
    """

    if is_secure:
        scheme = "https"
    else:
        scheme = "http"

    data = {
        "PROJECT": {
            "release": __version__,
            "release_base64": base64.urlsafe_b64encode(
                __version__.encode("utf-8")
            ).decode("utf-8"),
        },
    }

    if with_siteobject:
        site_current = Site.objects.get_current()
        data.update({
            "SITE": {
                "name": site_current.name,
                "domain": site_current.domain,
                "web_url": "{}://{}".format(scheme, site_current.domain),
                "scheme": scheme,
            },
        })

    if with_media:
        data["MEDIA_URL"] = getattr(settings, "MEDIA_URL", "")

    if with_static:
        data["STATIC_URL"] = getattr(settings, "STATIC_URL", "")

    if getattr(settings, "EXTRA_PROJECT_GLOBALS", None):
        data["EXTRA"] = getattr(settings, "EXTRA_PROJECT_GLOBALS")

    data.update(extra)

    return data


def project_globals(request):
    """
    Context processor to add the current project globals to the context.

    Args:
        request (object): A Django Request object to use its method ``is_secure``.

    Returns:
        dict: Global item to add to template context.
    """
    return get_project_globals(is_secure=request.is_secure())
