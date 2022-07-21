from django.urls import path
from . import views

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("signin/", views.sign_in, name="signin"),
    path("signout/", views.sign_out, name="signout"),
]
