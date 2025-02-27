from haystack import indexes

from .models import Assortment, Category, Consumable, Product
from .search_fields import EdgeNgramField


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = EdgeNgramField(
        document=True,
        use_template=True,
        template_name="atoum/search/base_field_indexes_template.txt"
    )

    def get_model(self):
        return Product


class AssortmentIndex(indexes.SearchIndex, indexes.Indexable):
    text = EdgeNgramField(
        document=True,
        use_template=True,
        template_name="atoum/search/base_field_indexes_template.txt"
    )

    def get_model(self):
        return Assortment


class ConsumableIndex(indexes.SearchIndex, indexes.Indexable):
    text = EdgeNgramField(
        document=True,
        use_template=True,
        template_name="atoum/search/base_field_indexes_template.txt"
    )

    def get_model(self):
        return Consumable


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = EdgeNgramField(
        document=True,
        use_template=True,
        template_name="atoum/search/base_field_indexes_template.txt"
    )

    def get_model(self):
        return Category
