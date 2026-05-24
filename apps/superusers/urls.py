from django.urls import path

from . import views

app_name = "superusers"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path("products/", views.products, name="products"),
    path("products/add/", views.add_product, name="add_product"),

    path("orders/", views.orders, name="orders"),

    path("discounts/", views.discounts, name="discounts"),

    path("branches/", views.branches, name="branches"),

    path("finance/", views.finance, name="finance"),

    path("hero/", views.hero_content, name="hero"),
]