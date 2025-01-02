from .assortment import AssortmentAdmin
from .brand import BrandAdmin
from .category import CategoryAdmin
from .consumable import ConsumableAdmin
from .product import ProductAdmin, ProductInline


__all__ = [
    "AssortmentAdmin",
    "BrandAdmin",
    "CategoryAdmin",
    "ConsumableAdmin",
    "ProductAdmin",
    "ProductInline",
]
