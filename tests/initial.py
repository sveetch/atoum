import shutil
from io import StringIO

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

    # We empty all description to avoid unexpected positive results on search tests
    steack = ProductFactory(
        category=beeffoods,
        title="Steack",
        slug="steack",
        brand=None,
        description=""
    )
    tongue = ProductFactory(
        category=beeffoods,
        title="Tongue",
        slug="tongue",
        brand=None,
        description=""
    )
    tbone = ProductFactory(
        category=beeffoods,
        title="T-Bone",
        slug="tbone",
        brand=None,
        description=""
    )
    wing = ProductFactory(
        category=chicken,
        title="Wing",
        slug="wing",
        brand=None,
        description=""
    )
    tomatoe = ProductFactory(
        category=reds,
        title="Tomatoe",
        slug="tomatoe",
        brand=None,
        description=""
    )
    corn = ProductFactory(
        category=yellows,
        title="Corn",
        slug="corn",
        brand=None,
        description=""
    )
    sensitive = ProductFactory(
        category=beefpets,
        title="Sensitive",
        slug="sensitive",
        brand=meowmax,
        description=""
    )
    other_product = ProductFactory(
        category=other_category,
        title="Other product",
        slug="other-product",
        brand=None,
        description=""
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
def index_catalog(settings):
    """
    Index catalog with Haystack.

    This is only useful if your test assert against search result else it would be
    useless.

    It may seems a little tricky but Haystack indexing processes are available from
    their Django command because do it programmatically seems very complicated.

    Finally this fixture assumes only a single backend (default) is configured.

    Returns:
        InitialCatalog: A dataclasses which contains every created model object.
    """
    # Ensure internal connection is rebooted. This is required because we directly
    # remove the backend index directory, else Haystack seems to keep reference or
    # pointer to the index and may fail or hang process.
    import haystack
    haystack.connections.reload("default")

    # Directly removes the directory instead of using 'clean_index' command, obviously
    # this would work only with Whoosh backend and it remove every backend indexes.
    if settings.HAYSTACK_CONNECTIONS["default"]["PATH"].exists():
        shutil.rmtree(settings.HAYSTACK_CONNECTIONS["default"]["PATH"])

    with StringIO() as out:
        args = [
            "--settings=sandbox.settings.tests",
        ]
        call_command("update_index", *args, stdout=out)
        content = out.getvalue()

    return content
