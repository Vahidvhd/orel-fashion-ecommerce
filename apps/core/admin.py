from django.contrib import admin

from apps.core.models import Branch, HeroContent


@admin.register(HeroContent)
class HeroContentAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "sort_order", "updated_at")
    list_filter = ("is_active",)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "phone", "is_active", "sort_order")
    list_filter = ("is_active", "country")
