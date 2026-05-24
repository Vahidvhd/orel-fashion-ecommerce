import json
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from apps.accounts.forms import LoginForm, RegistrationForm, VerificationForm
from apps.accounts.models import User
from apps.accounts.services import create_verification_code
from apps.cart.services import (
    add_to_cart,
    get_or_create_cart,
    merge_session_cart_to_user,
    remove_cart_item,
    update_cart_item,
)
from apps.catalog.filters import filter_products, get_active_discounts_for_product
from apps.catalog.models import Color, Product, ProductVariant, Size
from apps.core.models import Branch
from apps.orders.forms import ShippingForm
from apps.orders.models import Order
from apps.orders.services import create_order_from_cart, mock_stripe_payment


SECTION_MAP = {
    "new": "new",
    "men": "men",
    "women": "women",
    "kids": "kids",
    "sale": "sale",
}


@method_decorator(ratelimit(key="ip", rate="5/m", method="POST", block=True), name="dispatch")
class RegisterView(FormView):
    template_name = "storefront/auth/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("storefront:verify")

    def form_valid(self, form):
        user = form.save()
        self.request.session["pending_verification_email"] = user.email
        messages.success(self.request, "Account created. Please enter your verification code.")
        return redirect(f"{reverse('storefront:verify')}?email={user.email}")


@method_decorator(ratelimit(key="ip", rate="10/m", method="POST", block=True), name="dispatch")
class VerifyView(FormView):
    template_name = "storefront/auth/verify.html"
    form_class = VerificationForm
    success_url = reverse_lazy("storefront:login")

    def get_initial(self):
        email = self.request.GET.get("email") or self.request.session.get("pending_verification_email", "")
        return {"email": email}

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        messages.success(self.request, "Email verified. You can now sign in.")
        return super().form_valid(form)


class ResendVerificationView(View):
    def post(self, request):
        email = request.POST.get("email", "").lower()
        try:
            user = User.objects.get(email=email)
            if not user.is_verified:
                create_verification_code(user)
                messages.success(request, "A new verification code has been sent.")
        except User.DoesNotExist:
            messages.info(request, "If an account exists, a code has been sent.")
        return redirect(reverse("storefront:verify") + f"?email={email}")


@method_decorator(ratelimit(key="ip", rate="10/m", method="POST", block=True), name="dispatch")
class LoginView(FormView):
    template_name = "storefront/auth/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("storefront:home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        merge_session_cart_to_user(self.request, user)

        if user.role in ["owner", "finance", "sales", "inventory"]:
            return redirect("superusers:dashboard")

        return redirect("storefront:home")

class HomeView(TemplateView):
    template_name = "storefront/home.html"


class CategoryView(ListView):
    template_name = "storefront/category.html"
    context_object_name = "products"
    paginate_by = 20

    def get_section(self):
        section = self.kwargs.get("section") or self.request.GET.get("section") or "men"
        return SECTION_MAP.get(section, "men")

    def get_queryset(self):
        section = self.get_section()
        params = self.request.GET
        min_price = params.get("min_price")
        max_price = params.get("max_price")
        try:
            min_p = Decimal(min_price) if min_price else None
        except (InvalidOperation, TypeError):
            min_p = None
        try:
            max_p = Decimal(max_price) if max_price else None
        except (InvalidOperation, TypeError):
            max_p = None
        return filter_products(
            Product.objects.prefetch_related("images", "variants__color", "variants__size"),
            section=section,
            category_slug=params.get("category"),
            min_price=min_p,
            max_price=max_p,
            color_slugs=params.getlist("color"),
            size_slugs=params.getlist("size"),
            on_sale=params.get("sale") == "1" or section == "sale",
            sort=params.get("sort", "newest"),
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["section"] = self.get_section()
        ctx["section_label"] = self.get_section().title()
        ctx["colors"] = Color.objects.filter(is_active=True)
        ctx["sizes"] = Size.objects.filter(is_active=True)
        params = self.request.GET
        ctx["filters"] = params
        ctx["selected_colors"] = params.getlist("color")
        ctx["selected_sizes"] = params.getlist("size")
        return ctx


class ProductGridPartialView(CategoryView):
    """HTMX partial for dynamic filter updates."""

    template_name = "storefront/partials/product_grid.html"

    def dispatch(self, request, *args, **kwargs):
        kwargs["section"] = request.GET.get("section", "men")
        return super().dispatch(request, *args, **kwargs)


class ProductDetailView(DetailView):
    model = Product
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "storefront/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.prefetch_related(
            "images",
            "variants__color",
            "variants__size",
            "variants__discounts",
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        product = self.object
        variants = product.variants.filter(is_active=True).select_related("color", "size")
        ctx["variants"] = variants
        ctx["colors"] = Color.objects.filter(
            id__in=variants.values_list("color_id", flat=True),
            is_active=True,
        ).distinct()
        ctx["sizes"] = Size.objects.filter(
            id__in=variants.values_list("size_id", flat=True),
            is_active=True,
        ).distinct()
        ctx["discounts"] = get_active_discounts_for_product(product)
        variant_data = []
        for v in variants:
            d = v.active_discount
            variant_data.append(
                {
                    "id": v.id,
                    "color_slug": v.color.slug,
                    "size_slug": v.size.slug,
                    "price": str(v.effective_price),
                    "original_price": str(v.price),
                    "stock": v.stock,
                    "in_stock": v.is_in_stock,
                    "discount_ends": d.ends_at.isoformat() if d else None,
                }
            )
        ctx["variant_json"] = json.dumps(variant_data)
        return ctx


class SearchView(ListView):
    template_name = "storefront/search.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        if not q:
            return Product.objects.none()
        return Product.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q),
            is_active=True,
        ).prefetch_related("images")


class CartView(TemplateView):
    template_name = "storefront/cart.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        ctx["cart"] = cart
        ctx["items"] = cart.items.select_related(
            "variant__product",
            "variant__color",
            "variant__size",
        )
        return ctx


class CartAddView(View):
    def post(self, request):
        variant_id = request.POST.get("variant_id")
        quantity = int(request.POST.get("quantity", 1))
        variant = get_object_or_404(ProductVariant, pk=variant_id, is_active=True)
        cart = get_or_create_cart(request)
        try:
            add_to_cart(cart, variant, quantity)
            messages.success(request, "Added to bag.")
        except ValueError as e:
            messages.error(request, str(e))
        if request.headers.get("HX-Request"):
            return render(request, "storefront/partials/cart_badge.html")
        return redirect(request.POST.get("next") or reverse("storefront:cart"))


class CartUpdateView(View):
    def post(self, request, item_id):
        cart = get_or_create_cart(request)
        quantity = int(request.POST.get("quantity", 1))
        try:
            update_cart_item(cart, item_id, quantity)
        except ValueError as e:
            messages.error(request, str(e))
        if request.headers.get("HX-Request"):
            return render(
                request,
                "storefront/partials/cart_items.html",
                {"cart": cart, "items": cart.items.select_related("variant__product", "variant__color", "variant__size")},
            )
        return redirect("storefront:cart")


class CartRemoveView(View):
    def post(self, request, item_id):
        cart = get_or_create_cart(request)
        remove_cart_item(cart, item_id)
        if request.headers.get("HX-Request"):
            return render(
                request,
                "storefront/partials/cart_items.html",
                {"cart": cart, "items": cart.items.select_related("variant__product", "variant__color", "variant__size")},
            )
        return redirect("storefront:cart")


class CartBadgeView(View):
    def get(self, request):
        return render(request, "storefront/partials/cart_badge.html")


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = "storefront/checkout.html"
    form_class = ShippingForm
    login_url = reverse_lazy("storefront:login")

    def dispatch(self, request, *args, **kwargs):
        cart = get_or_create_cart(request)
        if not cart.items.exists():
            messages.warning(request, "Your bag is empty.")
            return redirect("storefront:cart")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        ctx["cart"] = cart
        ctx["items"] = cart.items.select_related("variant__product", "variant__color", "variant__size")
        ctx["stripe_public_key"] = self.request.settings.STRIPE_PUBLIC_KEY if hasattr(self.request, "settings") else ""
        from django.conf import settings

        ctx["stripe_public_key"] = settings.STRIPE_PUBLIC_KEY
        ctx["order_total"] = cart.subtotal + Decimal("4.99")
        return ctx

    def get_initial(self):
        user = self.request.user
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone_number,
        }

    def form_valid(self, form):
        self.request.session["shipping_data"] = form.cleaned_data
        return redirect("storefront:checkout_pay")


class CheckoutPayPageView(LoginRequiredMixin, TemplateView):
    template_name = "storefront/checkout_pay.html"
    login_url = reverse_lazy("storefront:login")

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("shipping_data"):
            return redirect("storefront:checkout")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        ctx["cart"] = cart
        return ctx


class CheckoutPaymentView(LoginRequiredMixin, View):
    login_url = reverse_lazy("storefront:login")

    def post(self, request):
        shipping_data = request.session.get("shipping_data")
        if not shipping_data:
            messages.error(request, "Please complete shipping information first.")
            return redirect("storefront:checkout")
        cart = get_or_create_cart(request)
        payment = mock_stripe_payment(cart.subtotal + Decimal("4.99"))
        order = create_order_from_cart(
            request.user,
            cart,
            shipping_data,
            payment_intent_id=payment["id"],
        )
        request.session.pop("shipping_data", None)
        messages.success(request, f"Order {order.order_number} placed successfully.")
        return redirect("storefront:order_detail", order_number=order.order_number)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "storefront/profile.html"
    login_url = reverse_lazy("storefront:login")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["orders"] = Order.objects.filter(user=self.request.user).prefetch_related("status_history")
        return ctx


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    slug_field = "order_number"
    slug_url_kwarg = "order_number"
    template_name = "storefront/order_detail.html"
    context_object_name = "order"
    login_url = reverse_lazy("storefront:login")

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items", "status_history")
