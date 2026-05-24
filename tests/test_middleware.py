import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestCountryRestrictionMiddleware:
    def test_login_blocked_outside_allowed_countries(self, client):
        response = client.get(
            reverse("storefront:login"),
            HTTP_X_COUNTRY_CODE="US",
        )
        assert response.status_code == 403

    def test_login_allowed_uk(self, client):
        response = client.get(
            reverse("storefront:login"),
            HTTP_X_COUNTRY_CODE="GB",
        )
        assert response.status_code == 200

    def test_login_allowed_iran(self, client):
        response = client.get(
            reverse("storefront:login"),
            HTTP_X_COUNTRY_CODE="IR",
        )
        assert response.status_code == 200

    def test_browsing_allowed_globally(self, client):
        response = client.get(
            reverse("storefront:home"),
            HTTP_X_COUNTRY_CODE="US",
        )
        assert response.status_code == 200
