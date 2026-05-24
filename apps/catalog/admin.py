from django.contrib import admin

from apps.catalog.models import (
    Category,
    Color,
    Discount,
    Product,
    ProductImage,
    ProductVariant,
    Size,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    autocomplete_fields = ("color", "size")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "gender", "is_active", "is_new_arrival", "created_at")
    list_filter = ("gender", "category", "is_active", "is_new_arrival")
    search_fields = ("title", "slug", "description")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("category",)
    inlines = [ProductImageInline, ProductVariantInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("product", "color", "size", "price", "stock", "is_active")
    list_filter = ("color", "size", "is_active")
    search_fields = ("sku", "product__title")
    autocomplete_fields = ("product", "color", "size")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "sort_order", "is_primary")


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "hex_code", "is_active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order", "is_active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "section", "parent", "is_active")
    list_filter = ("section", "is_active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("parent",)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("percentage", "product", "variant", "starts_at", "ends_at", "is_active")
    list_filter = ("is_active",)
    autocomplete_fields = ("product", "variant", "color", "size")
