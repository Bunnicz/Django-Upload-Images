# from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, UserTier


class CustomUserAdmin(UserAdmin):
    list_display = ["username", "tier", "is_superuser", "date_joined", "last_login"]
    readonly_fields = ["date_joined", "last_login"]
    search_fields = ["username"]
    date_hierarchy = "last_login"
    fieldsets = (("User Tier", {"fields": ("tier",)}),) + UserAdmin.fieldsets
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "tier",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


class UserTierAdmin(admin.ModelAdmin):
    list_display = ("name", "img_px200", "img_px400", "img_native", "generated_url")
    list_filter = ["img_px200", "img_px400", "img_native", "generated_url"]
    search_fields = ["name"]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserTier, UserTierAdmin)
