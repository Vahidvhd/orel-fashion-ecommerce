from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, VerificationCode


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "is_verified",
        "is_staff",
        "date_joined",
    )

    list_filter = (
        "role",
        "is_verified",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
    )

    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Profile", {"fields": ("role", "phone_number", "is_verified", "verified_at")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "created_at", "expires_at", "is_used")
    list_filter = ("is_used", "created_at")
    search_fields = ("user__email", "code")