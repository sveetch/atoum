
=========
Changelog
=========

Version 0.4.1 - 2025/04/30
**************************

* Search form now applies autofocus on query input if it is empty;
* Search form now makes all models as checked if none was checked;
* Simplified some view code with usage ``get_object_or_404``;
* Made some renaming so the vague term *opened shopping list* is renamed to
  *shopping inventory*;
* Implemented 'done' field control to update a product state;
* Changed shopping management so it work also from shopping detail and not anymore
  only from inventory;
* Refactored Shopping inventory and some related code;
* Dropped inventory dataclass in profit of Shopping model method with cache;
* Finished Shopping interface with htmx;


Version 0.4.0 - 2025/03/20
**************************

* Added Makefile tasks to manage search engine indexes;
* Improved some view tests to assert on amount of querysets to ensure we do not break
  performances;
* Added new behavior to Shopping list admin to set shopping list as done or undone
  depending the 'done state' of its items;
* Improved search implementation, this is a partial search and query is normalized
  (lowercase and accent removed);
* Implemented opened Shopping list management and interface with htmx library;
* Updated PO french catalog;
* Improved test coverage;
* Added children counts on list items for all index and detail views;
* Made some various minor fixes and improvements;


Version 0.3.0 - 2025/02/23
**************************

* Added ``django-view-breadcrumbs`` requirement and configuration;
* Added catalog views to browse into Consumables, Assortments, Categories and Products;
* Added major improvements to the sandbox layout;
* Added styleguide app to sandbox;
* Added search engine with ``django-haystack`` with ``Whoosh`` backend;
* Added export command which gather atoum model resources into a XSLX file;
* Added logo to documentation;


Version 0.2.0 - 2025/01/05
**************************

Not release as a package because it still is in an experimental phase.

* Added catalog models: Consumable, Assortment, Category, Product and Brand;
* Added new extra requirement section ``sandbox``, dedicated to dependencies only used
  in Sandbox;
* Added Diskette requirement to the extra ``sandbox`` requirements because it is only
  used in sandbox, it would be useless in package base requirements;
* Enabled Diskette for sandbox;
* Added 'prepopulated_fields' rule in admins for the slug fields;
* Added shopping models;
* Improved Admin forms;
* Added requirement ``django-autocomplete-light`` for better relation choice field into
  forms;
* Added test for models, forms, factories and autocompletes views;
* Added ``django-debug-toolbar`` with conditionnal config in demo settings and urls;


Version 0.1.0 - 2024/09/20
**************************

Initial commit from cookiecutter-sveetch-djangoapp v0.7.2

Not release as a package because it is in an experimental phase.