from django.dispatch import receiver
from django.shortcuts import redirect, render
from .models import MyUser
from django.contrib.auth.models import auth
from django.contrib import messages
from django.core.mail import send_mail
from .task import task_func

# Create your views here.


def signup(request):
    if request.method == "POST":
        first_name = request.POST["fn"]
        last_name = request.POST["ln"]
        user_name = request.POST["un"]
        user_email = request.POST["em"]
        password = request.POST["pwd"]
        c_password = request.POST["cpwd"]
        user_type = request.POST['au']

        if (
            MyUser.objects.filter(user_name=user_name).exists()
            or MyUser.objects.filter(user_email=user_email).exists()
        ):
            messages.warning(
                request,
                "user with same email or username already exists please login",
            )
            return redirect("sign-in")
        else:
            if password == c_password and user_type == 'Auther':
                user_object = MyUser.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    user_name=user_name,
                    user_email=user_email,
                    password=password,
                    is_auther=True,
                )
                user_object.save()
                messages.success(
                    request,
                    f"user with username:{user_name} registered please login",
                )
                user_object = MyUser.objects.filter(is_staff=True)
                task_func.delay(message='An auther wants to sign up',
                                title='New User request', receiver=[user.user_email for user in user_object])

                return redirect("sign-in")

            elif password == c_password and user_type == 'Reader':
                user_object = MyUser.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    user_name=user_name,
                    user_email=user_email,
                    password=password,
                    is_auther=False,
                )
                user_object.save()
                messages.success(
                    request,
                    f"user with username:{user_name} registered please login",
                )
                user_object = MyUser.objects.filter(is_staff=True)
                task_func.delay(message='An reader wants to sign up',
                                title='New User request', receiver=[user.user_email for user in user_object])

                return redirect("sign-in")

            elif password == c_password and user_type == 'Admin':
                user_object = MyUser.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    user_name=user_name,
                    user_email=user_email,
                    password=password,
                    is_staff=True,
                    is_superuser=True
                )
                user_object.save()
                messages.success(
                    request,
                    f"user with username:{user_name} registered please login",
                )
                user_object = MyUser.objects.filter(is_staff=True)
                task_func.delay(message='An admin wants to sign up',
                                title='New User request', receiver=[user.user_email for user in user_object])

                return redirect("sign-in")

            else:
                messages.warning(request, "password mismatch error")
                return redirect("signup")
    return render(request, "account/register.html")


def signin(request):
    if request.method == "POST":
        user_email = request.POST["em"]
        password = request.POST["pwd"]

        user_object = MyUser.objects.filter(user_email=user_email)

        if user_object.exists():

            if auth.authenticate(user_email=user_email, password=password):
                auth.login(
                    request, auth.authenticate(
                        user_email=user_email, password=password)
                )
                messages.success(request, "user loged in sucessfully")
                task_func.delay(message='You just signed in blogapi.in',
                                title='new signin', receiver=[user_email])

                return redirect("index")
            else:
                messages.warning(request, "password mismatch")
                return redirect("sign-in")
        else:
            messages.warning(
                request,
                f"user with email:{user_email} doess not exists",
            )
            return redirect("sign-in")
    return render(request, "account/login.html")


def sign_out(request):
    auth.logout(request)
    messages.success(request, "sucessfully loged out")

    return redirect("sign-in")
