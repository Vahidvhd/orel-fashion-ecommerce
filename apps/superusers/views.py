from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.catalog.models import Discount, Product
from apps.core.models import Branch, BusinessSettings, HeroContent, HomeFeatureCard
from apps.orders.models import Order

from .decorators import business_role_required
from .forms import (
    BranchForm,
    BusinessSettingsForm,
    HeroContentForm,
    HomeFeatureCardForm,
)


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
def website_settings(request):
    business_settings = BusinessSettings.get_settings()
    hero = HeroContent.objects.first()

    branch_id = request.GET.get("edit_branch")
    card_id = request.GET.get("edit_card")

    editing_branch = get_object_or_404(Branch, pk=branch_id) if branch_id else None
    editing_card = get_object_or_404(HomeFeatureCard, pk=card_id) if card_id else None

    settings_form = BusinessSettingsForm(instance=business_settings)
    hero_form = HeroContentForm(instance=hero)
    branch_form = BranchForm(instance=editing_branch)
    card_form = HomeFeatureCardForm(instance=editing_card)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "save_settings":
            settings_form = BusinessSettingsForm(request.POST, instance=business_settings)
            if settings_form.is_valid():
                settings_form.save()
                messages.success(request, "Business settings updated.")
                return redirect("superusers:website_settings")

        elif action == "save_hero":
            hero_form = HeroContentForm(request.POST, request.FILES, instance=hero)
            if hero_form.is_valid():
                hero_form.save()
                messages.success(request, "Hero content updated.")
                return redirect("superusers:website_settings")

        elif action == "save_branch":
            branch_pk = request.POST.get("branch_id")
            branch_instance = get_object_or_404(Branch, pk=branch_pk) if branch_pk else None
            branch_form = BranchForm(request.POST, instance=branch_instance)

            if branch_form.is_valid():
                branch_form.save()
                messages.success(request, "Branch saved.")
                return redirect("superusers:website_settings")

        elif action == "delete_branch":
            branch_pk = request.POST.get("branch_id")
            branch = get_object_or_404(Branch, pk=branch_pk)
            branch.delete()
            messages.success(request, "Branch deleted.")
            return redirect("superusers:website_settings")

        elif action == "save_card":
            card_pk = request.POST.get("card_id")
            card_instance = get_object_or_404(HomeFeatureCard, pk=card_pk) if card_pk else None
            card_form = HomeFeatureCardForm(request.POST, request.FILES, instance=card_instance)

            if card_form.is_valid():
                card_form.save()
                messages.success(request, "Home feature card saved.")
                return redirect("superusers:website_settings")

        elif action == "delete_card":
            card_pk = request.POST.get("card_id")
            card = get_object_or_404(HomeFeatureCard, pk=card_pk)
            card.delete()
            messages.success(request, "Home feature card deleted.")
            return redirect("superusers:website_settings")

    return render(request, "superusers/website_settings.html", {
        "business_settings": business_settings,
        "settings_form": settings_form,
        "hero": hero,
        "hero_form": hero_form,
        "branches": Branch.objects.all(),
        "branch_form": branch_form,
        "editing_branch": editing_branch,
        "home_feature_cards": HomeFeatureCard.objects.all(),
        "card_form": card_form,
        "editing_card": editing_card,
    })


@business_role_required(["owner"])
def branches(request):
    return redirect("superusers:website_settings")


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
    return redirect("superusers:website_settings")