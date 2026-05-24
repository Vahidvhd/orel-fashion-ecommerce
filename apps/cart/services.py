from decimal import Decimal

from django.conf import settings

from apps.cart.models import Cart, CartItem
from apps.catalog.models import ProductVariant


def get_or_create_cart(request) -> Cart:
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart


def merge_session_cart_to_user(request, user) -> None:
    if not request.session.session_key:
        return
    session_cart = Cart.objects.filter(session_key=request.session.session_key, user=None).first()
    if not session_cart:
        return
    user_cart, _ = Cart.objects.get_or_create(user=user)
    for item in session_cart.items.all():
        existing = user_cart.items.filter(variant=item.variant).first()
        if existing:
            existing.quantity += item.quantity
            existing.save(update_fields=["quantity"])
        else:
            item.cart = user_cart
            item.save(update_fields=["cart"])
    session_cart.delete()


def add_to_cart(cart: Cart, variant: ProductVariant, quantity: int = 1) -> CartItem:
    if not variant.is_in_stock:
        raise ValueError("Variant is out of stock")
    if quantity > variant.stock:
        raise ValueError("Insufficient stock")
    unit_price = variant.effective_price
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={"quantity": quantity, "unit_price": unit_price},
    )
    if not created:
        new_qty = item.quantity + quantity
        if new_qty > variant.stock:
            raise ValueError("Insufficient stock")
        item.quantity = new_qty
        item.unit_price = unit_price
        item.save(update_fields=["quantity", "unit_price"])
    return item


def update_cart_item(cart: Cart, item_id: int, quantity: int) -> CartItem | None:
    try:
        item = cart.items.get(pk=item_id)
    except CartItem.DoesNotExist:
        return None
    if quantity <= 0:
        item.delete()
        return None
    if quantity > item.variant.stock:
        raise ValueError("Insufficient stock")
    item.quantity = quantity
    item.unit_price = item.variant.effective_price
    item.save(update_fields=["quantity", "unit_price"])
    return item


def remove_cart_item(cart: Cart, item_id: int) -> bool:
    deleted, _ = cart.items.filter(pk=item_id).delete()
    return deleted > 0


def get_cart_count(request) -> int:
    cart = get_or_create_cart(request)
    return cart.item_count
