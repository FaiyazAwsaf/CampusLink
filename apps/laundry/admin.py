from django.contrib import admin
from .models import LaundryCategory, LaundryOrder, LaundryOrderItem

class LaundryOrderItemInline(admin.TabularInline):
    model = LaundryOrderItem
    extra = 0
    readonly_fields = ('subtotal',)

@admin.register(LaundryCategory)
class LaundryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'wash_price', 'ironing_price', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('name',)

@admin.register(LaundryOrder)
class LaundryOrderAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'user', 'total_amount', 'total_items', 'status', 'estimated_delivery_date', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('invoice_number', 'user__name', 'user__email')
    readonly_fields = ('invoice_number', 'total_amount', 'total_items', 'estimated_delivery_date')
    inlines = [LaundryOrderItemInline]
    date_hierarchy = 'created_at'
