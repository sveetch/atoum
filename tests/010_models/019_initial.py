from tests.initial import initial_catalog


def test_factory_creation(db, initial_catalog):
    """
    Initial catalog should correctly create a catalog structure as expected.
    """
    assert initial_catalog.get_ascii_tree() == (
        "───<Consumable: Food>\n"
        "   └─<Assortment: Meat>\n"
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
