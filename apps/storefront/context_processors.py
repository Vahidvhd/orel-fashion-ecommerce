from django.conf import settings

from apps.core.models import Branch, HeroContent


def brand_context(request):
    return {
        "brand_name": settings.BRAND_NAME,
        "active_hero": HeroContent.objects.filter(is_active=True).first(),
        "branches": Branch.objects.filter(is_active=True)[:6],
    }
