"""
TODO
"""
import json
from pathlib import Path

import yaml

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from atoum.models import Assortment, Category, Consumable, Product


class Command(BaseCommand):
    """
    TODO:
    """
    def add_arguments(self, parser):
        pass

    def get_products(self, category, products):
        for item in products:
            product = Product(
                category=category,
                title=item,
                slug=slugify(item)
            )
            product.save()
            print("         └─ Product:", item, slugify(item))

        return

    def get_categories(self, assortment, categories):

        if isinstance(categories, dict):
            items = categories.items()
        else:
            items = categories

        for item in items:
            name = item
            products = None

            if isinstance(item, tuple):
                name = item[0]
                products = item[1]

            category = Category(
                assortment=assortment,
                title=name,
                slug=slugify(name)
            )
            category.save()
            print("      └─ Cat:", name, slugify(name))
            if products:
                self.get_products(category, products)

        return

    def get_assortments(self, consumable, assortments):
        for name, categories in assortments.items():
            assortment = Assortment(
                consumable=consumable,
                title=name,
                slug=slugify(name)
            )
            assortment.save()
            print("   └─ Gamme:", name, slugify(name))
            if categories:
                self.get_categories(assortment, categories)

        return

    def get_consumables(self, classification):
        for name, assortments in classification.items():
            consumable = Consumable(title=name, slug=slugify(name))
            consumable.save()
            print("└─ Conso:", name, slugify(name))

            self.get_assortments(consumable, assortments)

        return

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=== Classification ==="))

        # Relative to command current path (not relative to this script)
        SOURCE_PATH = Path("classification.yaml")

        self.stdout.write("Parsing file:{}".format(SOURCE_PATH))

        classification = yaml.safe_load(SOURCE_PATH.read_text())

        self.stdout.write(json.dumps(classification, indent=4))

        self.stdout.write()
        self.stdout.write(self.style.SUCCESS("=== Parsed tree ==="))

        self.get_consumables(classification)
