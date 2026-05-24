from django.contrib import admin

from apps.orders.models import Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_title", "color_name", "size_name", "sku", "quantity", "unit_price", "line_total")


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ("status", "note", "created_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "user", "status", "total", "payment_status", "created_at")
    list_filter = ("status", "payment_status")
    search_fields = ("order_number", "user__email", "shipping_email")
    readonly_fields = ("order_number", "created_at", "updated_at")
    inlines = [OrderItemInline, OrderStatusHistoryInline]

    def save_model(self, request, obj, form, change):
        if change:
            old = Order.objects.get(pk=obj.pk)
            if old.status != obj.status:
                OrderStatusHistory.objects.create(
                    order=obj,
                    status=obj.status,
                    note=f"Updated by {request.user.email}",
                )
        super().save_model(request, obj, form, change)
