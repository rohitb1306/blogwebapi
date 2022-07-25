from django.contrib import admin  # noqa
from .models import Blog, Comment


class BlogAdmin(admin.ModelAdmin):
    search_fields = ("blog_title", "blog_auther")
    ordering = ("-blog_uploaded_on",)
    list_filter = ("blog_new_request",)
    list_display = ("blog_title", "blog_auther",
                    "blog_new_request", "blog_is_approved")
    filter_horizontal = ()

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "blog_auther",
                    "blog_image",
                    "blog_content",
                    "blog_title",
                    "blog_description",
                    "blog_keywords",
                )
            },
        ),
        (
            "permissions",
            {"fields": ("blog_is_approved", "blog_new_request",
                        "blog_del_request")},
        ),
    )


# Register your models here.
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
