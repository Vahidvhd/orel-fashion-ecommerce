import pytest
from django.test import client as django_test_client


@pytest.fixture(autouse=True)
def _disable_template_context_copy():
    """Avoid Python 3.14 + Django template Context __copy__ incompatibility in tests."""
    original = django_test_client.store_rendered_templates

    def noop(*args, **kwargs):
        return None

    django_test_client.store_rendered_templates = noop
    yield
    django_test_client.store_rendered_templates = original


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def iran_request_factory():
    from django.test import RequestFactory

    factory = RequestFactory()

    def _make(path="/accounts/login/", method="get"):
        request = getattr(factory, method)(path)
        request.META["HTTP_X_COUNTRY_CODE"] = "IR"
        return request

    return _make
