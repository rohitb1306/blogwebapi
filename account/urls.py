from django.urls import path
from . import views

urlpatterns = [
    path("sign-up", views.Signup.as_view(), name="sign-up"),
    path("sign-out", views.Signout.as_view(), name="sign-out"),
    path(
        "profile/<slug>", views.Profile.as_view(), name="show-profile"
    ),
    path(
        "update-profile/<slug>",
        views.Update_profile.as_view(),
        name="update-profile",
    ),
    path("profile/",views.Profileaccount.as_view(),name="profile")
]
