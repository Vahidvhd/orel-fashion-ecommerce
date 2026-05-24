"""
Geo-IP abstraction for country detection.

Production: use CF-IPCountry, X-Country-Code, or a GeoIP2 database.
Development: GEOIP_DEFAULT_COUNTRY or X-Debug-Country header.
"""
from django.conf import settings


class GeoIPService:
    HEADER_PRIORITY = (
        "HTTP_CF_IPCOUNTRY",
        "HTTP_X_COUNTRY_CODE",
        "HTTP_X_DEBUG_COUNTRY",
    )

    @classmethod
    def get_country_code(cls, request) -> str:
        for header in cls.HEADER_PRIORITY:
            value = request.META.get(header, "").strip().upper()
            if value and value != "XX":
                return value
        return getattr(settings, "GEOIP_DEFAULT_COUNTRY", "GB").upper()

    @classmethod
    def is_auth_allowed(cls, request) -> bool:
        country = cls.get_country_code(request)
        allowed = [c.upper() for c in settings.ALLOWED_AUTH_COUNTRIES]
        return country in allowed
