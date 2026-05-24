from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    hex_code = models.CharField(max_length=7, default="#000000")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Section(models.TextChoices):
        NEW = "new", "New"
        MEN = "men", "Men"
        WOMEN = "women", "Women"
        KIDS = "kids", "Kids"
        SALE = "sale", "Sale"

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    section = models.CharField(max_length=20, choices=Section.choices)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["section", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Gender(models.TextChoices):
        MEN = "men", "Men"
        WOMEN = "women", "Women"
        KIDS = "kids", "Kids"
        UNISEX = "unisex", "Unisex"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    gender = models.CharField(max_length=20, choices=Gender.choices)
    is_active = models.BooleanField(default=True)
    is_new_arrival = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def primary_image(self):
        return self.images.filter(is_primary=True).first() or self.images.first()

    @property
    def min_price(self):
        prices = [v.effective_price for v in self.variants.filter(is_active=True)]
        return min(prices) if prices else Decimal("0.00")


    @property
    def has_active_discount(self):
        now = timezone.now()

        return Discount.objects.filter(
            models.Q(product=self) | models.Q(variant__product=self),
            is_active=True,
            starts_at__lte=now,
            ends_at__gte=now,
        ).exists()


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="products/%Y/%m/")
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.product.title} - image {self.pk}"


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    sku = models.CharField(max_length=64, unique=True, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["color__name", "size__sort_order"]
        unique_together = [["product", "color", "size"]]

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"{self.product.slug}-{self.color.slug}-{self.size.slug}"[:64]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.title} - {self.color.name} / {self.size.name}"

    @property
    def is_in_stock(self):
        return self.stock > 0 and self.is_active

    @property
    def active_discount(self):
        now = timezone.now()
        return (
            self.discounts.filter(
                is_active=True,
                starts_at__lte=now,
                ends_at__gte=now,
            )
            .order_by("-percentage")
            .first()
        )

    @property
    def effective_price(self):
        discount = self.active_discount
        if discount:
            return discount.discounted_price(self.price)
        return self.price

    @property
    def discount_percentage(self):
        discount = self.active_discount
        return discount.percentage if discount else 0


class Discount(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="discounts",
        null=True,
        blank=True,
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="discounts",
        null=True,
        blank=True,
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="discounts",
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="discounts",
    )
    percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Discount percentage (1-99)",
    )
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    label = models.CharField(max_length=100, default="Limited time deal")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-starts_at"]

    def __str__(self):
        target = self.variant or self.product or "global"
        return f"{self.percentage}% off {target}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.ends_at <= self.starts_at:
            raise ValidationError("End time must be after start time.")
        if self.percentage >= 100:
            raise ValidationError("Percentage must be less than 100.")

    @property
    def is_currently_active(self):
        now = timezone.now()
        return self.is_active and self.starts_at <= now <= self.ends_at

    def discounted_price(self, original_price):
        multiplier = Decimal(100 - self.percentage) / Decimal(100)
        return (original_price * multiplier).quantize(Decimal("0.01"))

    def applies_to_variant(self, variant):
        if not self.is_currently_active:
            return False
        if self.variant_id:
            return self.variant_id == variant.id
        if self.product_id and self.product_id != variant.product_id:
            return False
        if self.color_id and self.color_id != variant.color_id:
            return False
        if self.size_id and self.size_id != variant.size_id:
            return False
        return bool(self.variant_id or self.product_id or self.color_id or self.size_id)
