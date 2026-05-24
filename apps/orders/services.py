from decimal import Decimal

from django.db import transaction

from apps.cart.models import Cart
from apps.orders.models import Order, OrderItem, OrderStatusHistory


SHIPPING_COST = Decimal("4.99")


def create_order_from_cart(user, cart: Cart, shipping_data: dict, payment_intent_id: str = "") -> Order:
    if not cart.items.exists():
        raise ValueError("Cart is empty")

    with transaction.atomic():
        subtotal = cart.subtotal
        total = subtotal + SHIPPING_COST
        order = Order.objects.create(
            user=user,
            shipping_first_name=shipping_data["first_name"],
            shipping_last_name=shipping_data["last_name"],
            shipping_email=shipping_data["email"],
            shipping_phone=shipping_data["phone"],
            shipping_address_line1=shipping_data["address_line1"],
            shipping_address_line2=shipping_data.get("address_line2", ""),
            shipping_city=shipping_data["city"],
            shipping_postcode=shipping_data["postcode"],
            shipping_country=shipping_data.get("country", "United Kingdom"),
            subtotal=subtotal,
            shipping_cost=SHIPPING_COST,
            total=total,
            stripe_payment_intent_id=payment_intent_id,
            payment_status="confirmed",
            status=Order.Status.PAYMENT_CONFIRMED,
        )
        for item in cart.items.select_related("variant__product", "variant__color", "variant__size"):
            variant = item.variant
            variant.stock = max(0, variant.stock - item.quantity)
            variant.save(update_fields=["stock"])
            OrderItem.objects.create(
                order=order,
                product_title=variant.product.title,
                color_name=variant.color.name,
                size_name=variant.size.name,
                sku=variant.sku,
                quantity=item.quantity,
                unit_price=item.unit_price,
                line_total=item.line_total,
            )
        OrderStatusHistory.objects.create(
            order=order,
            status=Order.Status.ORDER_PLACED,
            note="Order created",
        )
        OrderStatusHistory.objects.create(
            order=order,
            status=Order.Status.PAYMENT_CONFIRMED,
            note="Payment confirmed",
        )
        cart.items.all().delete()
    return order


def mock_stripe_payment(amount: Decimal, currency: str = "gbp") -> dict:
    """Test-mode placeholder payment flow."""
    return {
        "id": f"pi_mock_{int(amount * 100)}",
        "status": "succeeded",
        "amount": int(amount * 100),
        "currency": currency,
        "client_secret": "mock_secret_placeholder",
    }
