from decimal import Decimal

import pytest
from django.utils import timezone
from datetime import timedelta

from apps.catalog.filters import filter_products
from apps.catalog.models import Category, Color, Discount, Product, ProductVariant, Size


@pytest.fixture
def catalog_setup(db):
    color = Color.objects.create(name="Black", hex_code="#000")
    size_s = Size.objects.create(name="S", sort_order=1)
    size_m = Size.objects.create(name="M", sort_order=2)
    cat = Category.objects.create(name="Coats", section=Category.Section.MEN)
    product = Product.objects.create(
        title="Wool Coat",
        description="Warm coat",
        category=cat,
        gender="men",
        is_new_arrival=True,
    )
    v1 = ProductVariant.objects.create(product=product, color=color, size=size_s, price=Decimal("100"), stock=5)
    v2 = ProductVariant.objects.create(product=product, color=color, size=size_m, price=Decimal("120"), stock=0)
    return product, v1, v2, color, size_s, size_m


@pytest.mark.django_db
class TestProductFiltering:
    def test_filter_by_color(self, catalog_setup):
        product, v1, v2, color, size_s, size_m = catalog_setup
        qs = filter_products(Product.objects.all(), color_slugs=[color.slug])
        assert product in qs

    def test_filter_by_price_range(self, catalog_setup):
        product, v1, v2, color, size_s, size_m = catalog_setup
        qs = filter_products(Product.objects.all(), min_price=Decimal("110"))
        assert product in qs
        qs_high = filter_products(Product.objects.all(), min_price=Decimal("200"))
        assert product not in qs_high

    def test_sort_price_asc(self, catalog_setup):
        product, v1, v2, color, size_s, size_m = catalog_setup
        qs = filter_products(Product.objects.all(), sort="price_asc")
        assert list(qs)[0] == product


@pytest.mark.django_db
class TestDiscounts:
    def test_active_discount(self, catalog_setup):
        product, v1, v2, color, size_s, size_m = catalog_setup
        now = timezone.now()
        Discount.objects.create(
            variant=v1,
            percentage=20,
            starts_at=now - timedelta(hours=1),
            ends_at=now + timedelta(days=1),
        )
        assert v1.effective_price == Decimal("80.00")
        assert v1.active_discount.is_currently_active
