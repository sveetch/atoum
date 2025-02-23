import pytest

from django.core.management import call_command

from atoum.factories import (
    AssortmentFactory, BrandFactory, CategoryFactory, ConsumableFactory, ProductFactory
)
from atoum.utils.dataset import InitialCatalog


@pytest.fixture(scope="function")
def initial_catalog(db):
    """
    Build some various objects for a basic catalog.

    Returns:
        InitialCatalog: A dataclasses which contains every created model object.
    """
    foods = ConsumableFactory(title="Food", slug="foods")
    pets = ConsumableFactory(title="Pets", slug="pets")
    hygiene = ConsumableFactory(title="Hygiene", slug="hygiene")
    other_consumable = ConsumableFactory(
        title="Other consumable",
        slug="other-consumable"
    )

    meats = AssortmentFactory(consumable=foods, title="Meats", slug="meats")
    vegetables = AssortmentFactory(
        consumable=foods,
        title="Vegetables",
        slug="vegetables"
    )
    sweettreats = AssortmentFactory(
        consumable=foods,
        title="Sweat treats",
        slug="sweet-treats"
    )
    croquettes = AssortmentFactory(
        consumable=pets,
        title="Croquettes",
        slug="croquettes"
    )
    other_assortment = AssortmentFactory(
        consumable=other_consumable,
        title="Other assortment",
        slug="other-assortment"
    )

    beeffoods = CategoryFactory(assortment=meats, title="Beef", slug="beef")
    pig = CategoryFactory(assortment=meats, title="Pig", slug="pig")
    chicken = CategoryFactory(assortment=meats, title="Chicken", slug="chicken")
    beefpets = CategoryFactory(assortment=croquettes, title="Beef", slug="beef")
    yellows = CategoryFactory(assortment=vegetables, title="Yellows", slug="yellows")
    reds = CategoryFactory(assortment=vegetables, title="Reds", slug="reds")
    other_category = CategoryFactory(
        assortment=other_assortment,
        title="Other category",
        slug="other-category"
    )

    meowmax = BrandFactory(title="Meow MAX", slug="meow-max")

    steack = ProductFactory(
        category=beeffoods,
        title="Steack",
        slug="steack",
        brand=None
    )
    tongue = ProductFactory(
        category=beeffoods,
        title="Tongue",
        slug="tongue",
        brand=None
    )
    tbone = ProductFactory(
        category=beeffoods,
        title="T-Bone",
        slug="tbone",
        brand=None
    )
    wing = ProductFactory(
        category=chicken,
        title="Wing",
        slug="wing",
        brand=None
    )
    tomatoe = ProductFactory(
        category=reds,
        title="Tomatoe",
        slug="tomatoe",
        brand=None
    )
    corn = ProductFactory(
        category=yellows,
        title="Corn",
        slug="corn",
        brand=None
    )
    sensitive = ProductFactory(
        category=beefpets,
        title="Sensitive",
        slug="sensitive",
        brand=meowmax
    )
    other_product = ProductFactory(
        category=other_category,
        title="Other product",
        slug="other-product",
        brand=None
    )

    return InitialCatalog(
        consumables={
            "foods": foods,
            "pets": pets,
            "hygiene": hygiene,
            "other_consumable": other_consumable,
        },
        assortments={
            "meats": meats,
            "vegetables": vegetables,
            "sweettreats": sweettreats,
            "croquettes": croquettes,
            "other_assortment": other_assortment,
        },
        brands={
            "meowmax": meowmax,
        },
        categories={
            "beeffoods": beeffoods,
            "pig": pig,
            "chicken": chicken,
            "beefpets": beefpets,
            "other_category": other_category,
        },
        products={
            "steack": steack,
            "tongue": tongue,
            "tbone": tbone,
            "tomatoe": tomatoe,
            "corn": corn,
            "sensitive": sensitive,
            "wing": wing,
            "other_product": other_product,
        },
    )


@pytest.fixture(scope="function")
def index_initial_catalog(initial_catalog):
    """
    Invoke "initial_catalog" to build catalog then index it with Haystack.

    This is only useful if your test assert against search result else it would be
    useless.

    It may be a little tricky but Haystack indexing processes are only properly
    available from their Django command, this is the only way to do it on demand
    (instead of a pre processed index shipped in test data).

    Returns:
        InitialCatalog: A dataclasses which contains every created model object.
    """
    from io import StringIO

    with StringIO() as out:
        args = [
            "--noinput",
            "--settings=sandbox.settings.tests",
        ]
        call_command("clear_index", *args, stdout=out)
        # print(out.getvalue())
        # print("-"*40)

    with StringIO() as out:
        args = [
            "--settings=sandbox.settings.tests",
        ]
        call_command("update_index", *args, stdout=out)
        # print(out.getvalue())
        # print("-"*40)

    return initial_catalog
