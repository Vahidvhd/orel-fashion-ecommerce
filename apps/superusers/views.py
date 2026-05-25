from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.catalog.models import Discount, Product
from apps.core.models import Branch, BusinessSettings, HeroContent
from apps.orders.models import Order

from .decorators import business_role_required
from .forms import BranchForm, BusinessSettingsForm, HeroContentForm


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
    business_settings = BusinessSettings.get_settings()
    branch_id = request.GET.get("edit")
    editing_branch = None

    if branch_id:
        editing_branch = get_object_or_404(Branch, pk=branch_id)

    settings_form = BusinessSettingsForm(instance=business_settings)
    branch_form = BranchForm(instance=editing_branch)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "save_settings":
            settings_form = BusinessSettingsForm(request.POST, instance=business_settings)
            if settings_form.is_valid():
                settings_form.save()
                messages.success(request, "Business settings updated.")
                return redirect("superusers:branches")

        elif action == "save_branch":
            branch_pk = request.POST.get("branch_id")
            branch_instance = None

            if branch_pk:
                branch_instance = get_object_or_404(Branch, pk=branch_pk)

            branch_form = BranchForm(request.POST, instance=branch_instance)
            if branch_form.is_valid():
                branch_form.save()
                messages.success(request, "Branch saved.")
                return redirect("superusers:branches")

        elif action == "delete_branch":
            branch_pk = request.POST.get("branch_id")
            branch = get_object_or_404(Branch, pk=branch_pk)
            branch.delete()
            messages.success(request, "Branch deleted.")
            return redirect("superusers:branches")

    return render(request, "superusers/branches.html", {
        "branches": Branch.objects.all(),
        "business_settings": business_settings,
        "settings_form": settings_form,
        "branch_form": branch_form,
        "editing_branch": editing_branch,
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