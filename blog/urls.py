from django.urls import path
from . import views

urlpatterns = [
    # path("", views.Addblog.as_view(), name="addblog"),
    path("", views.Add_blog.as_view(), name="add-blog"),
    path("my-blog", views.My_blog.as_view(), name="My-blog"),
    # path(
    #     "updateblog1/<slug>",
    #     views.Blogupdate1.as_view(),
    #     name="updateblog1",
    # ),
    path(
        "updateblog/<slug>", views.Blogupdate.as_view(), name="updateblog"
    ),
    path(
        "deleteblog/<slug>", views.Blogdelete.as_view(), name="deleteblog"
    ),
    path("open-blog/<slug>", views.Open_blog.as_view(), name="open-blog"),
    path(
        "addcomment/<slug>", views.Addcomment.as_view(), name="addcomment"
    ),
]
