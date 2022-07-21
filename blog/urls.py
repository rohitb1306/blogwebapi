from django.urls import path
from . import views

urlpatterns = [
    path("", views.blogupload, name="addblog"),
    path("updateblog1", views.blogupdate1, name="updateblog1"),
    path("updateblog/<bid>", views.blogupdate, name="updateblog"),
    path("deleteblog/<bid>", views.blogdelete, name="deleteblog"),
    path("open_blog/<bid>", views.open_blog, name="open_blog"),
    path("addcomment/<bid>", views.addcomment, name="addcomment"),
]
