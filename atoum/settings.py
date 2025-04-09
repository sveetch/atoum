"""
Default application settings
----------------------------

These are the default settings you can override in your own project settings
right after the line which load the default app settings.

"""

ATOUM_ASSORTMENT_PAGINATION = 30
"""
Assortment per page limit for pagination, set it to ``None`` to disable
pagination.
"""

ATOUM_CATEGORY_PAGINATION = 25
"""
Category per page limit for pagination, set it to ``None`` to disable
pagination.
"""

ATOUM_PRODUCT_PAGINATION = 50
"""
Product per page limit for pagination, set it to ``None`` to disable
pagination.
"""

ATOUM_SHOPPINGLIST_PAGINATION = 9
"""
Shopping per page limit for pagination, set it to ``None`` to disable
pagination.
"""

ATOUM_BREADCRUMBS_SHOW_HOME = True
"""
If breadcrumbs should include the site homepage entry or not. This is only working
in Atoum views.
"""

ATOUM_INDEXES_DEBUG = False
"""
When enabled, the build and update of search indexes will output every rendered content
for indexed objects.

This can be huge if you have hundreds or more objects to index.
"""

ATOUM_SHOPPING_ASIDE_TEMPLATE = "atoum/shopping/partials/tag_shopping_aside_html.html"
"""
Template path used to render A Shopping list as aside content. This is used when
user has opened a Shopping list in 'selection' mode.
"""

ATOUM_SHOPPING_PRODUCT_CONTROLS_TEMPLATE = (
    "atoum/product/partials/shopping_product_controls.html"
)
"""
Template path used to render product controls for a possible opened Shopping list.
"""
