from django.urls import path

from . import views

app_name = "superusers"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path("products/", views.products, name="products"),
    path("products/add/", views.add_product, name="add_product"),

    path("orders/", views.orders, name="orders"),

    path("discounts/", views.discounts, name="discounts"),

    path("website-settings/", views.website_settings, name="website_settings"),

    path("branches/", views.branches, name="branches"),
    path("hero/", views.hero_content, name="hero"),

    path("finance/", views.finance, name="finance"),
]