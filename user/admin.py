from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from user.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom UserAdmin for email-based authentication (no username field)."""
    
    # Fields to display in the user list
    list_display = ('email', 'first_name', 'last_name', 'is_customer', 'is_manager', 'is_admin', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_customer', 'is_manager', 'is_admin', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    # Fieldsets for user detail/edit page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_customer', 'is_manager', 'is_admin', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fieldsets for creating new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_customer', 'is_manager', 'is_admin'),
        }),
    )
    
    # Remove username from required fields
    readonly_fields = ('date_joined', 'last_login')


