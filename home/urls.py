from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("admin_custom", views.Admin.as_view(), name="admin_custom"),
    # path("admin2", views.admin2, name="admin2"),
    path(
        "userapproval/<uid>",
        views.Userapproval.as_view(),
        name="userapproval",
    ),
    path(
        "blog-W-U-approval/<slug>",
        views.Blogapproval.as_view(),
        name="blog-W-U-approval",
    ),
    path(
        "blog-D-approval/<slug>",
        views.Blog_delete_approval.as_view(),
        name="blog-D-approval",
    ),
    path("search", views.Searching.as_view(), name="search"),
    path("search1/<search>", views.Search1.as_view(), name="search1"),
    path(
        "blog-download",
        views.Blog_download.as_view(),
        name="blog-download",
    ),
    path(
        "blog-csv/<fromtime>/<totime>/<mail>",
        views.Blog_csv.as_view(),
        name="blog-csv",
    ),
    path(
        "blog-pdf/<fromtime>/<totime>/<mail>",
        views.Blog_pdf.as_view(),
        name="blog-pdf",
    ),
]
