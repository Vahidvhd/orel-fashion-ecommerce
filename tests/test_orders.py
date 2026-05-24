import pytest
from decimal import Decimal
from django.test import Client
from django.urls import reverse

from apps.accounts.models import User
from apps.cart.services import add_to_cart, get_or_create_cart
from apps.catalog.models import Category, Color, Product, ProductVariant, Size
from apps.orders.models import Order
from apps.orders.services import create_order_from_cart, mock_stripe_payment


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="buyer@example.com",
        email="buyer@example.com",
        password="testpass123",
        first_name="Buyer",
        last_name="Test",
        is_verified=True,
    )


@pytest.fixture
def cart_with_item(user, db):
    from apps.cart.models import Cart

    color = Color.objects.create(name="White", hex_code="#fff")
    size = Size.objects.create(name="L", sort_order=1)
    cat = Category.objects.create(name="Tops", section=Category.Section.WOMEN)
    product = Product.objects.create(
        title="Blouse",
        description="Silk blouse",
        category=cat,
        gender="women",
    )
    variant = ProductVariant.objects.create(
        product=product, color=color, size=size, price=Decimal("80"), stock=5
    )
    cart, _ = Cart.objects.get_or_create(user=user)
    add_to_cart(cart, variant, 1)
    return cart, user


@pytest.mark.django_db
class TestCheckout:
    def test_mock_payment(self):
        result = mock_stripe_payment(Decimal("100.00"))
        assert result["status"] == "succeeded"

    def test_create_order(self, cart_with_item):
        cart, user = cart_with_item
        shipping = {
            "first_name": "Buyer",
            "last_name": "Test",
            "email": user.email,
            "phone": "+44000000000",
            "address_line1": "1 Test St",
            "city": "London",
            "postcode": "W1A 1AA",
        }
        order = create_order_from_cart(user, cart, shipping, payment_intent_id="pi_test")
        assert order.status == Order.Status.PAYMENT_CONFIRMED
        assert order.items.count() == 1
        assert cart.items.count() == 0

    def test_order_tracking_page(self, client, user, cart_with_item):
        cart, user = cart_with_item
        order = create_order_from_cart(
            user,
            cart,
            {
                "first_name": "B",
                "last_name": "T",
                "email": user.email,
                "phone": "123",
                "address_line1": "1 St",
                "city": "London",
                "postcode": "E1",
            },
        )
        client.force_login(user)
        response = client.get(
            reverse("storefront:order_detail", kwargs={"order_number": order.order_number}),
            HTTP_X_COUNTRY_CODE="GB",
        )
        assert response.status_code == 200
        assert order.order_number.encode() in response.content


@pytest.mark.django_db
class TestAdminProduct:
    def test_admin_product_creation(self, db):
        from apps.catalog.models import Category, Product

        cat = Category.objects.create(name="Jeans", section=Category.Section.MEN)
        product = Product.objects.create(
            title="Admin Product",
            description="Created via admin workflow",
            category=cat,
            gender="men",
        )
        assert Product.objects.filter(pk=product.pk).exists()
