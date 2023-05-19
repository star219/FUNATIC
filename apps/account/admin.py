from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import UserAccount
from .forms import UserCreateForm


class UserAccountAdmin(UserAdmin):
    add_form = UserCreateForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_display_links = ('username','first_name', 'last_name')
    list_filter = ('is_active', 'is_staff')
    ordering = ['-id']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ('date_joined',)
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            }
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2")
            }
        ),
    )

admin.site.register(UserAccount, UserAccountAdmin)