from tests.initial import initial_catalog  # noqa: F401


def test_factory_creation(db, initial_catalog):  # noqa: F811
    """
    Initial catalog should correctly create a catalog structure as expected.

    .. Todo::
        We should check also the Brands that are in their own tree.
    """
    assert initial_catalog.get_ascii_tree() == (
        "───<Consumable: Food>\n"
        "   └─<Assortment: Meats>\n"
        "      └─<Category: Beef>\n"
        "         └─<Product: Steack>\n"
        "         └─<Product: T-Bone>\n"
        "         └─<Product: Tongue>\n"
        "      └─<Category: Chicken>\n"
        "         └─<Product: Wing>\n"
        "      └─<Category: Pig>\n"
        "   └─<Assortment: Sweat treats>\n"
        "   └─<Assortment: Vegetables>\n"
        "      └─<Category: Reds>\n"
        "         └─<Product: Tomatoe>\n"
        "      └─<Category: Yellows>\n"
        "         └─<Product: Corn>\n"
        "───<Consumable: Pets>\n"
        "   └─<Assortment: Croquettes>\n"
        "      └─<Category: Beef>\n"
        "         └─<Product: Sensitive>\n"
        "───<Consumable: Hygiene>"
    )
