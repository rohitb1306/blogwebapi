from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin_custom", views.admin, name="admin_custom"),
    path("userapproval/<uid>", views.userapproval, name="userapproval"),
    path(
        "blog-W-U-approval/<slug>",
        views.blogapproval,
        name="blog-W-U-approval",
    ),
    path(
        "blog-D-approval/<slug>",
        views.blog_Delete_approval,
        name="blog-D-approval",
    ),
    path("about", views.about, name="about"),
    path("search", views.search, name="search"),
    path("search1/<search>", views.search1, name="search1"),
]
