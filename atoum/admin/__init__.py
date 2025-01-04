from .assortment import AssortmentAdmin
from .brand import BrandAdmin
from .category import CategoryAdmin
from .consumable import ConsumableAdmin
from .product import ProductAdmin, ProductAdminInline
from .shopping import ShoppingAdmin


__all__ = [
    "AssortmentAdmin",
    "BrandAdmin",
    "CategoryAdmin",
    "ConsumableAdmin",
    "ProductAdmin",
    "ProductAdminInline",
    "ShoppingAdmin",
]
