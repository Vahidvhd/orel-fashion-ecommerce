import pytest
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from freezegun import freeze_time

from apps.catalog.models import Category, Color, Discount, Product, ProductVariant, Size


@pytest.mark.django_db
class TestDiscountTimer:
    def test_discount_end_time_available_for_countdown(self):
        color = Color.objects.create(name="Red", hex_code="#f00")
        size = Size.objects.create(name="M", sort_order=1)
        cat = Category.objects.create(name="Sale", section=Category.Section.SALE)
        product = Product.objects.create(
            title="Sale Item",
            description="On sale",
            category=cat,
            gender="women",
        )
        variant = ProductVariant.objects.create(
            product=product, color=color, size=size, price=Decimal("100"), stock=5
        )
        ends = timezone.now() + timedelta(hours=2)
        discount = Discount.objects.create(
            variant=variant,
            percentage=15,
            starts_at=timezone.now() - timedelta(minutes=5),
            ends_at=ends,
        )
        assert discount.is_currently_active
        with freeze_time(timezone.now() + timedelta(hours=3)):
            assert not discount.is_currently_active
