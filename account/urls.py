from django.urls import path
from . import views

urlpatterns = [
    path("sign-up", views.signup, name="sign-up"),
    path("sign-in", views.signin, name="sign-in"),
    path("sign-out", views.sign_out, name="sign-out"),
]
