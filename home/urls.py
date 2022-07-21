from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin_custom", views.admin, name="admin_custom"),
    path("userapproval/<uid>", views.userapproval, name="userapproval"),
    path(
        "blog_W-U_approval/<bid>",
        views.blogapproval,
        name="blog_W-U_approval",
    ),
    path(
        "blog_D_approval/<bid>",
        views.blog_Delete_approval,
        name="blog_D_approval",
    ),
    path("about", views.about, name="about"),

]
