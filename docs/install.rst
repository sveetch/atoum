.. _install_intro:

=======
Install
=======

Install package in your environment : ::

    pip install atoum[breadcrumbs]

For development usage see :ref:`development_install`.

Configuration
*************

Add it to your installed Django apps in settings : ::

    INSTALLED_APPS = (
        ...
        "atoum",
    )

Then load default application settings in your settings file: ::

    from atoum.settings import *

Then mount applications URLs: ::

    urlpatterns = [
        ...
        path("", include("atoum.urls")),
    ]

And finally apply database migrations.

Settings
********

.. automodule:: atoum.settings
   :members:
