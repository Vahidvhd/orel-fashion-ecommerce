import pytest
from decimal import Decimal
from django.test import Client
from django.urls import reverse

from apps.cart.services import add_to_cart, get_or_create_cart
from apps.catalog.models import Category, Color, Product, ProductVariant, Size


@pytest.fixture
def variant(db):
    color = Color.objects.create(name="Navy", hex_code="#001")
    size = Size.objects.create(name="M", sort_order=1)
    cat = Category.objects.create(name="Shirts", section=Category.Section.MEN)
    product = Product.objects.create(
        title="Shirt",
        description="Cotton shirt",
        category=cat,
        gender="men",
    )
    return ProductVariant.objects.create(
        product=product, color=color, size=size, price=Decimal("50"), stock=10
    )


@pytest.fixture
def cart_for_session(db, client):
    from django.contrib.auth.models import AnonymousUser
    from django.test import RequestFactory

    client.get("/")
    factory = RequestFactory()
    request = factory.get("/")
    request.session = client.session
    request.user = AnonymousUser()
    return get_or_create_cart(request)


@pytest.mark.django_db
class TestCart:
    def test_add_to_cart(self, cart_for_session, variant):
        cart = cart_for_session
        add_to_cart(cart, variant, 2)
        assert cart.item_count == 2

    def test_cart_badge_shows_count(self, client, cart_for_session, variant):
        cart = cart_for_session
        add_to_cart(cart, variant, 1)
        response = client.get(reverse("storefront:cart_badge"))
        assert response.status_code == 200
        assert b"1" in response.content

    def test_cart_badge_with_items(self, client, cart_for_session, variant):
        cart = cart_for_session
        add_to_cart(cart, variant, 3)
        response = client.get(reverse("storefront:cart_badge"))
        assert b"3" in response.content
