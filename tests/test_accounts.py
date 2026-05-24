import pytest
from django.core import mail
from django.test import Client
from django.urls import reverse

from apps.accounts.models import User, VerificationCode
from apps.accounts.services import create_verification_code, verify_code


@pytest.mark.django_db
class TestRegistration:
    def test_registration_form_creates_user(self, db):
        from unittest.mock import patch

        from apps.accounts.forms import RegistrationForm

        with patch("apps.accounts.forms.random.randint", side_effect=[3, 5]):
            form = RegistrationForm(
                {
                    "name": "John",
                    "surname": "Smith",
                    "phone_number": "+447700900000",
                    "email": "john@example.com",
                    "password": "securepass123",
                    "password_confirm": "securepass123",
                    "captcha": "8",
                }
            )
        assert form.is_valid(), form.errors
        user = form.save()
        assert user.email == "john@example.com"
        assert user.is_verified is False


@pytest.mark.django_db
class TestVerification:
    def test_verification_code_flow(self):
        user = User.objects.create_user(
            username="verify@example.com",
            email="verify@example.com",
            password="testpass123",
            first_name="V",
            last_name="User",
        )
        verification = create_verification_code(user)
        assert VerificationCode.objects.filter(user=user, is_used=False).exists()
        assert verify_code(user, verification.code)
        user.refresh_from_db()
        assert user.is_verified


@pytest.mark.django_db
class TestLogin:
    def test_login_requires_verification(self, client):
        user = User.objects.create_user(
            username="login@example.com",
            email="login@example.com",
            password="testpass123",
            first_name="L",
            last_name="User",
            is_verified=False,
        )
        response = client.post(
            reverse("storefront:login"),
            {"username": "login@example.com", "password": "testpass123"},
            HTTP_X_COUNTRY_CODE="GB",
        )
        assert response.status_code == 200

    def test_verified_user_can_login(self, client):
        user = User.objects.create_user(
            username="ok@example.com",
            email="ok@example.com",
            password="testpass123",
            first_name="O",
            last_name="K",
            is_verified=True,
        )
        response = client.post(
            reverse("storefront:login"),
            {"username": "ok@example.com", "password": "testpass123"},
            HTTP_X_COUNTRY_CODE="GB",
        )
        assert response.status_code == 302
