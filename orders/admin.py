from django.contrib import admin

from .models import Order, ProductPurchase


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'status', 'total', 'phone', 'customer_email', 'timestamp')
    list_filter = ('status',)
    search_fields = ('order_id', 'phone', 'billing_profile__email')
    readonly_fields = ('timestamp', 'updated')

    def customer_email(self, obj):
        return obj.billing_profile.email if obj.billing_profile else ''


admin.site.register(ProductPurchase)
