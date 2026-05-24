from django.urls import path

from apps.api import views

app_name = "api"

urlpatterns = [
    path("products/", views.ProductListAPIView.as_view(), name="product_list"),
    path("products/<slug:slug>/", views.ProductDetailAPIView.as_view(), name="product_detail"),
    path("cart/count/", views.CartCountAPIView.as_view(), name="cart_count"),
    path("discounts/active/", views.ActiveDiscountsAPIView.as_view(), name="active_discounts"),
]
