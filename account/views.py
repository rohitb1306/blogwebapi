from django.shortcuts import redirect
from .models import MyUser
from django.contrib.auth.models import auth
from django.contrib import messages
from .task import task_func
from django.views.generic.base import TemplateView, View,RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView,UpdateView

from .forms import signupform,updateprofileform

# Create your views here.

class Signup(CreateView):
    form_class = signupform
    template_name = "account/register.html"
    success_url='login'

    def form_valid(self, form):
        messages.success(self.request,'User added send for admin approval')
        task_func.delay(
                message="A User wants to signin",
                title="new user Request",
                receiver=[user.user_email for user in MyUser.objects.isstaff()],
            )
        return super().form_valid(form)

# class Signin(TemplateView):
#     template_name = "account/login.html"

#     def post(self, request):
#         user_email = request.POST["em"]
#         password = request.POST["pwd"]

#         user_object = MyUser.objects.filter(user_email=user_email)

#         if user_object.exists():

#             if auth.authenticate(user_email=user_email, password=password):
#                 auth.login(
#                     request,
#                     auth.authenticate(
#                         user_email=user_email, password=password
#                     ),
#                 )
#                 messages.success(request, "user loged in sucessfully")
#                 task_func.delay(
#                     message="You just signed in blogapi.in",
#                     title="new signin",
#                     receiver=[user_email],
#                 )

#                 return redirect("index")
#             else:
#                 messages.warning(request, "password mismatch")
#                 return redirect("sign-in")
#         else:
#             messages.warning(
#                 request,
#                 f"user with email:{user_email} doess not exists",
#             )
#             return redirect("sign-in")


class Signout(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, "successfully loged out")
        return redirect("login")


class Profile(DetailView):
    template_name = "account/profile.html"
    model = MyUser

class Update_profile(UpdateView):
    form_class = updateprofileform
    template_name = "account/update.html"
    success_url='/'
    model=MyUser

class Profileaccount(RedirectView):
    url='/'