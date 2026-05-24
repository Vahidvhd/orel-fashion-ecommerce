from decimal import Decimal

from django.db.models import DecimalField, OuterRef, Q, Subquery
from django.utils import timezone

from apps.catalog.models import Discount, ProductVariant


def get_sale_product_ids():
    now = timezone.now()
    product_ids = set()

    discounts = Discount.objects.filter(
        is_active=True,
        starts_at__lte=now,
        ends_at__gte=now,
    ).select_related("product", "variant", "color", "size")

    for discount in discounts:
        if discount.product_id:
            product_ids.add(discount.product_id)

        if discount.variant_id:
            product_ids.add(discount.variant.product_id)

        variant_qs = ProductVariant.objects.filter(is_active=True)

        if discount.product_id:
            variant_qs = variant_qs.filter(product_id=discount.product_id)

        if discount.color_id:
            variant_qs = variant_qs.filter(color_id=discount.color_id)

        if discount.size_id:
            variant_qs = variant_qs.filter(size_id=discount.size_id)

        if discount.color_id or discount.size_id:
            product_ids.update(variant_qs.values_list("product_id", flat=True))

    return product_ids


def filter_products(
    queryset,
    *,
    section=None,
    category_slug=None,
    gender=None,
    min_price=None,
    max_price=None,
    color_slugs=None,
    size_slugs=None,
    on_sale=False,
    sort="newest",
):
    qs = queryset.filter(is_active=True)

    if section:
        if section == "new":
            qs = qs.filter(is_new_arrival=True)
        elif section == "sale":
            qs = qs.filter(id__in=get_sale_product_ids())
        else:
            qs = qs.filter(Q(gender=section) | Q(category__section=section))

    if gender:
        qs = qs.filter(gender=gender)

    if category_slug:
        qs = qs.filter(category__slug=category_slug)

    matching_variants = ProductVariant.objects.filter(is_active=True)

    if color_slugs:
        matching_variants = matching_variants.filter(color__slug__in=color_slugs)

    if size_slugs:
        matching_variants = matching_variants.filter(size__slug__in=size_slugs)

    if min_price is not None:
        matching_variants = matching_variants.filter(price__gte=Decimal(str(min_price)))

    if max_price is not None:
        matching_variants = matching_variants.filter(price__lte=Decimal(str(max_price)))

    qs = qs.filter(id__in=matching_variants.values("product_id"))

    if on_sale:
        qs = qs.filter(id__in=get_sale_product_ids())

    min_price_subquery = matching_variants.filter(
        product_id=OuterRef("pk")
    ).order_by("price").values("price")[:1]

    max_price_subquery = matching_variants.filter(
        product_id=OuterRef("pk")
    ).order_by("-price").values("price")[:1]

    qs = qs.annotate(
        display_price=Subquery(min_price_subquery, output_field=DecimalField()),
        display_max_price=Subquery(max_price_subquery, output_field=DecimalField()),
    )

    if sort == "price_asc":
        return qs.order_by("display_price", "id")

    if sort == "price_desc":
        return qs.order_by("-display_max_price", "id")

    return qs.order_by("-created_at", "id")


def get_active_discounts_for_product(product):
    now = timezone.now()

    return Discount.objects.filter(
        Q(product=product)
        | Q(variant__product=product)
        | Q(color__productvariant__product=product)
        | Q(size__productvariant__product=product),
        is_active=True,
        starts_at__lte=now,
        ends_at__gte=now,
    ).distinct().select_related("variant", "color", "size")