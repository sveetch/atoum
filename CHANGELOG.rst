
=========
Changelog
=========

Development
***********

* Added ``django-view-breadcrumbs`` requirement and configuration;
* Added catalog views to browse into Consumables, Assortments, Categories and Products;


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