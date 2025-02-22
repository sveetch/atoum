import pytest

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

    meats = AssortmentFactory(
        consumable=foods,
        title="Meats",
        slug="meats"
    )
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

    beeffoods = CategoryFactory(assortment=meats, title="Beef", slug="beef")
    pig = CategoryFactory(assortment=meats, title="Pig", slug="pig")
    chicken = CategoryFactory(assortment=meats, title="Chicken", slug="chicken")
    beefpets = CategoryFactory(assortment=croquettes, title="Beef", slug="beef")
    yellows = CategoryFactory(assortment=vegetables, title="Yellows", slug="yellows")
    reds = CategoryFactory(assortment=vegetables, title="Reds", slug="reds")

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

    return InitialCatalog(
        consumables={
            "foods": foods,
            "pets": pets,
            "hygiene": hygiene,
        },
        assortments={
            "meats": meats,
            "vegetables": vegetables,
            "sweettreats": sweettreats,
            "croquettes": croquettes,
        },
        brands={
            "meowmax": meowmax,
        },
        categories={
            "beeffoods": beeffoods,
            "pig": pig,
            "chicken": chicken,
            "beefpets": beefpets,
        },
        products={
            "steack": steack,
            "tongue": tongue,
            "tbone": tbone,
            "tomatoe": tomatoe,
            "corn": corn,
            "sensitive": sensitive,
            "wing": wing,
        },
    )
