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

Search engine
*************

The search engine needs data indexes to work, it is not continuously updated when you
are changing your data, at least you first need to start indexes: ::

    make search-build

And then when your data changes, you may update indexes: ::

    make search-update

This is probably something you will have to automatize with scheduling tasks like Cron
or something else.


Settings
********

.. automodule:: atoum.settings
   :members:
