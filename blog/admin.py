from django.contrib import admin  # noqa
from .models import Blog, Comment, Search


class BlogAdmin(admin.ModelAdmin):
    ordering = ("-blog_uploaded_on",)
    list_filter = ("blog_new_request",)

    def blog_content_(self, obj):
        return obj.blog_content[:30]

    list_display = (
        "blog_title",
        "blog_auther",
        "blog_content_",
        "blog_is_approved",
        "blog_uploaded_on"
        
    )

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
            {
                "fields": (
                    (
                        "blog_is_approved",
                        "blog_new_request",
                        "blog_del_request",
                    ),
                )
            },
        ),
    )

    list_per_page = 20


# Register your models here.
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
admin.site.register(Search)
