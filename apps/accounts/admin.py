from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'name', 'is_admin', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_admin', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'phone', 'image')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_admin', 'is_staff', 'is_superuser', 'is_active')}
        ),
    )
    filter_horizontal = ('groups', 'user_permissions',)
