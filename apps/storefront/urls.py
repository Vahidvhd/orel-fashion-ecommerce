from django.contrib.auth import views as auth_views
from django.urls import path

from apps.storefront import views

app_name = "storefront"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("shop/<str:section>/", views.CategoryView.as_view(), name="category"),
    path("product/<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("search/", views.SearchView.as_view(), name="search"),
    # Auth
    path("accounts/register/", views.RegisterView.as_view(), name="register"),
    path("accounts/verify/", views.VerifyView.as_view(), name="verify"),
    path("accounts/resend/", views.ResendVerificationView.as_view(), name="resend_verification"),
    path("accounts/login/", views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/profile/", views.ProfileView.as_view(), name="profile"),
    path("accounts/orders/<str:order_number>/", views.OrderDetailView.as_view(), name="order_detail"),
    # Cart
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/add/", views.CartAddView.as_view(), name="cart_add"),
    path("cart/update/<int:item_id>/", views.CartUpdateView.as_view(), name="cart_update"),
    path("cart/remove/<int:item_id>/", views.CartRemoveView.as_view(), name="cart_remove"),
    path("cart/badge/", views.CartBadgeView.as_view(), name="cart_badge"),
    # Checkout
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("checkout/pay/", views.CheckoutPayPageView.as_view(), name="checkout_pay"),
    path("checkout/pay/confirm/", views.CheckoutPaymentView.as_view(), name="checkout_pay_confirm"),
    # HTMX partials
    path("partials/products/", views.ProductGridPartialView.as_view(), name="product_grid_partial"),
]
