from django.shortcuts import redirect, render

from apps.catalog.models import Product, Discount
from apps.core.models import Branch, HeroContent
from apps.orders.models import Order

from .decorators import business_role_required
from .forms import HeroContentForm


@business_role_required(["owner", "finance", "sales", "inventory"])
def dashboard(request):
    return render(request, "superusers/dashboard.html")


@business_role_required(["owner", "sales", "inventory"])
def products(request):
    return render(request, "superusers/products.html", {
        "products": Product.objects.all(),
    })


@business_role_required(["owner", "finance", "sales"])
def orders(request):
    return render(request, "superusers/orders.html", {
        "orders": Order.objects.all(),
    })


@business_role_required(["owner", "sales"])
def discounts(request):
    return render(request, "superusers/discounts.html", {
        "discounts": Discount.objects.all(),
    })


@business_role_required(["owner"])
def branches(request):
    return render(request, "superusers/branches.html", {
        "branches": Branch.objects.all(),
    })


@business_role_required(["owner", "finance"])
def finance(request):
    return render(request, "superusers/finance.html", {
        "orders": Order.objects.all(),
    })


@business_role_required(["owner", "sales", "inventory"])
def add_product(request):
    return render(request, "superusers/add_product.html")


@business_role_required(["owner", "sales"])
def hero_content(request):
    hero = HeroContent.objects.first()

    if request.method == "POST":
        form = HeroContentForm(request.POST, request.FILES, instance=hero)
        if form.is_valid():
            form.save()
            return redirect("superusers:hero")
    else:
        form = HeroContentForm(instance=hero)

    return render(request, "superusers/hero.html", {
        "form": form,
        "hero": hero,
    })