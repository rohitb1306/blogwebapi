from django.urls import path
from . import views

urlpatterns = [
    path("", views.blogupload, name="addblog"),
    path("updateblog1/<slug>", views.blogupdate1, name="updateblog1"),
    path("updateblog/<slug>", views.blogupdate, name="updateblog"),
    path("deleteblog/<slug>", views.blogdelete, name="deleteblog"),
    path("open-blog/<slug>", views.open_blog, name="open-blog"),
    path("addcomment/<slug>", views.addcomment, name="addcomment"),
]
