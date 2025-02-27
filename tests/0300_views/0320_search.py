from django.urls import reverse

from atoum.utils.tests import html_pyquery

from tests.initial import initial_catalog, index_catalog  # noqa: F401


def parse_result_items(elements):
    """
    Function helper to parse result item content.

    Arguments:
        elements (list): List of HtmlElement nodes.

    Returns:
        tuple: Respectively found Title, Model and possibly Parent (Always null for
        Consumable)
    """
    return [
        (
            v.cssselect(".title")[0].text,
            # model has no simple text but instead a mix with a tag
            v.cssselect(".model")[0].text_content().strip(),
            # Consumable doesnt have parent
            (
                v.cssselect(".parent")[0].text_content().strip()
                if v.cssselect(".parent")
                else None
            ),
        )
        for v in elements
    ]


def test_index_empty(client, db):  # noqa: F811
    """
    Search view should just respond with an empty message without any results.
    """
    url = reverse("atoum:search-results")
    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    assert len(dom.find(".search-results .results")) == 0
    assert len(dom.find(".search-results .empty")) == 1


def test_index_basic(client, db, initial_catalog, index_catalog):  # noqa: F811
    """
    At least two characters are needed else search engine don't process anything and
    there is no results. With minimal characters requirement the query should result
    for expected items.
    """

    url = reverse("atoum:search-results")
    response = client.get(url, data={"q": "b"})
    assert response.status_code == 200
    dom = html_pyquery(response)
    assert len(dom.find(".search-results .results .item")) == 0

    response = client.get(url, data={"q": "be"})
    assert response.status_code == 200
    dom = html_pyquery(response)
    assert parse_result_items(dom.find(".search-results .results .item")) == [
        ("Beef", "Category", "In assortment Meats"),
        ("Beef", "Category", "In assortment Croquettes"),
    ]


def test_index_models(client, db, initial_catalog, index_catalog,  # noqa: F811
                      django_assert_num_queries):
    """
    Search engine can gather results from different models.
    """
    url = reverse("atoum:search-results")

    # With all model enabled (default)
    # Use a queryset per model
    with django_assert_num_queries(4):
        response = client.get(url, data={"q": "other"})

    assert response.status_code == 200
    dom = html_pyquery(response)
    assert parse_result_items(dom.find(".search-results .results .item")) == [
        ("Other product", "Product", "In category Other category"),
        ("Other category", "Category", "In assortment Other assortment"),
        ("Other assortment", "Assortment", "In consumable Other consumable"),
        ("Other consumable", "Consumable", None),
    ]

    # With a few set of models selected
    with django_assert_num_queries(2):
        response = client.get(url, data={
            "q": "other",
            "models": ["atoum.category", "atoum.product"]
        })
    assert response.status_code == 200
    dom = html_pyquery(response)
    assert parse_result_items(dom.find(".search-results .results .item")) == [
        ("Other product", "Product", "In category Other category"),
        ("Other category", "Category", "In assortment Other assortment"),
    ]
