from django.contrib import admin

from apps.core.models import Branch, BusinessSettings, HeroContent, HomeFeatureCard


@admin.register(HeroContent)
class HeroContentAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "sort_order", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle")


@admin.register(HomeFeatureCard)
class HomeFeatureCardAdmin(admin.ModelAdmin):
    list_display = ("title", "label", "active", "sort_order")
    list_filter = ("active",)
    search_fields = ("title", "label")
    list_editable = ("active", "sort_order")


@admin.register(BusinessSettings)
class BusinessSettingsAdmin(admin.ModelAdmin):
    list_display = ("store_type", "updated_at")

    def has_add_permission(self, request):
        return not BusinessSettings.objects.exists()


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "phone", "active", "sort_order")
    list_filter = ("active", "country")
    search_fields = ("name", "address", "city", "postcode", "phone", "email")
    list_editable = ("active", "sort_order")