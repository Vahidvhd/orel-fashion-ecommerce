import json

from django.http import HttpResponseForbidden
from django.urls import resolve

from apps.core.geoip import GeoIPService

AUTH_PATH_PREFIXES = (
    "/accounts/login",
    "/accounts/register",
    "/accounts/verify",
    "/accounts/resend",
    "/api/auth/",
)


class CountryRestrictionMiddleware:
    """
    Restrict login/register to Iran (IR) and United Kingdom (GB) only.
    Browsing the store remains available globally.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._is_auth_route(request) and not GeoIPService.is_auth_allowed(request):
            if request.headers.get("HX-Request"):
                return HttpResponseForbidden("Access restricted in your region.")
            if request.path.startswith("/api/"):
                return HttpResponseForbidden(
                    json.dumps({"detail": "Authentication is not available in your region."}),
                    content_type="application/json",
                )
            from django.shortcuts import render

            return render(
                request,
                "storefront/auth/country_restricted.html",
                status=403,
            )
        return self.get_response(request)

    def _is_auth_route(self, request) -> bool:
        path = request.path
        if any(path.startswith(prefix) for prefix in AUTH_PATH_PREFIXES):
            return True
        try:
            match = resolve(path)
            return match.url_name in {
                "login",
                "register",
                "verify",
                "resend_verification",
            }
        except Exception:
            return False
