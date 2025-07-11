from django.contrib import admin
from .models import LaundryCategory, LaundryInvoice

@admin.register(LaundryCategory)
class LaundryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "wash_price", "iron_price", "active")
    list_filter = ("active",)
    search_fields = ("name",)

@admin.register(LaundryInvoice)
class LaundryInvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_cost', 'order_date', 'delivery_date')
    search_fields = ('user__username',)
    readonly_fields = ('items_json',)
