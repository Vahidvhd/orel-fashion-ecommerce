from decimal import Decimal

from django.db.models import Min, Q
from django.utils import timezone

from apps.catalog.models import Discount, Product, ProductVariant


def filter_products(
    queryset,
    *,
    section=None,
    category_slug=None,
    min_price=None,
    max_price=None,
    color_slugs=None,
    size_slugs=None,
    on_sale=False,
    sort="newest",
):
    qs = queryset.filter(is_active=True).distinct()

    if section:
        if section == "new":
            qs = qs.filter(is_new_arrival=True)
        elif section == "sale":
            now = timezone.now()
            qs = qs.filter(
                variants__discounts__is_active=True,
                variants__discounts__starts_at__lte=now,
                variants__discounts__ends_at__gte=now,
            ).distinct()
        else:
            qs = qs.filter(gender=section) | qs.filter(category__section=section)

    if category_slug:
        qs = qs.filter(category__slug=category_slug)

    variant_q = Q(variants__is_active=True)
    if color_slugs:
        variant_q &= Q(variants__color__slug__in=color_slugs)
    if size_slugs:
        variant_q &= Q(variants__size__slug__in=size_slugs)
    if min_price is not None:
        variant_q &= Q(variants__price__gte=Decimal(str(min_price)))
    if max_price is not None:
        variant_q &= Q(variants__price__lte=Decimal(str(max_price)))
    if on_sale:
        now = timezone.now()
        variant_q &= Q(
            variants__discounts__is_active=True,
            variants__discounts__starts_at__lte=now,
            variants__discounts__ends_at__gte=now,
        )

    qs = qs.filter(variant_q).annotate(min_variant_price=Min("variants__price"))

    if sort == "price_asc":
        qs = qs.order_by("min_variant_price")
    elif sort == "price_desc":
        qs = qs.order_by("-min_variant_price")
    else:
        qs = qs.order_by("-created_at")

    return qs.distinct()


def get_active_discounts_for_product(product):
    now = timezone.now()
    return Discount.objects.filter(
        Q(product=product) | Q(variant__product=product),
        is_active=True,
        starts_at__lte=now,
        ends_at__gte=now,
    ).select_related("variant", "color", "size")
