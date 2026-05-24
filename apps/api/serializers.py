from rest_framework import serializers

from apps.catalog.models import Color, Discount, Product, ProductImage, ProductVariant, Size


class StrictSerializer(serializers.ModelSerializer):
    """DRF serializers with strict field validation (Zod-like behavior)."""

    def run_validation(self, data=...):
        if data is ...:
            data = self.initial_data
        if not isinstance(data, dict):
            raise serializers.ValidationError("Expected a JSON object.")
        unknown = set(data.keys()) - set(self.fields.keys())
        if unknown:
            raise serializers.ValidationError({k: "Unknown field." for k in unknown})
        return super().run_validation(data)


class ColorSerializer(StrictSerializer):
    class Meta:
        model = Color
        fields = ("id", "name", "slug", "hex_code")


class SizeSerializer(StrictSerializer):
    class Meta:
        model = Size
        fields = ("id", "name", "slug")


class ProductImageSerializer(StrictSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "alt_text", "sort_order", "is_primary")


class ProductVariantSerializer(StrictSerializer):
    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    effective_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductVariant
        fields = (
            "id",
            "sku",
            "color",
            "size",
            "price",
            "effective_price",
            "stock",
            "is_in_stock",
            "discount_percentage",
        )


class ProductListSerializer(StrictSerializer):
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    primary_image_url = serializers.SerializerMethodField()
    has_discount = serializers.BooleanField(source="has_active_discount", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "slug",
            "gender",
            "min_price",
            "primary_image_url",
            "has_discount",
            "is_new_arrival",
        )

    def get_primary_image_url(self, obj):
        img = obj.primary_image
        if img and img.image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(img.image.url)
            return img.image.url
        return ""


class ProductDetailSerializer(ProductListSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    description = serializers.CharField()

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + (
            "description",
            "images",
            "variants",
            "created_at",
        )


class DiscountSerializer(StrictSerializer):
    ends_at = serializers.DateTimeField()
    starts_at = serializers.DateTimeField()

    class Meta:
        model = Discount
        fields = ("id", "percentage", "label", "starts_at", "ends_at", "product", "variant")
