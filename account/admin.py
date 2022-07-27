from attr import fields
from django.contrib import admin  # noqa
from .models import MyUser
from django.contrib.auth.admin import UserAdmin
import pdb


class UserAdminConfig(UserAdmin):
    search_fields = ("user_email", "user_name", "first_name", "is_auther")
    ordering = ("-sign_up_date",)
    list_filter = ("is_active", "is_auther", "is_staff", "is_superuser")
    list_display = (
        "user_email",
        "user_name",
        "first_name",
        "is_active",
        "is_staff",
        "is_auther",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_email",
                    "user_name",
                    "first_name",
                    "last_name",
                    "user_image",
                )
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_auther",
                    "is_superuser"
                )
            },
        ),
        (
            "advance_option",
            {
                "classes": ('collapse',), "fields": ('groups', 'user_permissions',)
            }
        )
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'user_email',
                'user_name',
                'first_name',
                'last_name',
                'user_contact',
                'is_auther',
                'is_staff',
                'is_superuser',
                'is_active',
                'password1',
                'password2',
                'user_image',
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        super(UserAdminConfig, self).save_model(request, obj, form, change)
        


# Register your models here.
admin.site.register(MyUser, UserAdminConfig)
