from django.conf import settings

from apps.core.models import Branch, BusinessSettings, HeroContent


def brand_context(request):
    business_settings = BusinessSettings.get_settings()

    return {
        "brand_name": settings.BRAND_NAME,
        "active_hero": HeroContent.objects.filter(is_active=True).first(),
        "business_settings": business_settings,
        "show_branches": business_settings.is_physical_store,
        "branches": Branch.objects.filter(active=True)[:6]
        if business_settings.is_physical_store
        else [],
    }