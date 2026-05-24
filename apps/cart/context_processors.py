from apps.cart.services import get_cart_count


def cart_context(request):
    return {"cart_item_count": get_cart_count(request)}
