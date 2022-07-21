from django.contrib import admin  # noqa
from .models import MyUser
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    search_fields = ("user_email", "user_name", "first_name", "is_auther")
    ordering = ("-sign_up_date",)
    list_filter = ("is_active", "is_auther", "is_staff")
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
    )


# Register your models here.
admin.site.register(MyUser, UserAdminConfig)
