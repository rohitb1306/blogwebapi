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
                if len(request.FILES) != 0:
                    image = request.FILES["im"]
                    user_object = MyUser.objects.get(user_email=user_email)
                    user_object.user_image = image
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
                if len(request.FILES) != 0:
                    image = request.FILES["im"]
                    user_object = MyUser.objects.get(user_email=user_email)
                    user_object.user_image = image
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
                if len(request.FILES) != 0:
                    image = request.FILES["im"]
                    user_object = MyUser.objects.get(user_email=user_email)
                    user_object.user_image = image
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
                return redirect("sign-up")
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


def profile(request):
    return render(request, 'account/profile.html')


def update_profile(request, slug):
    if request.method == "POST":
        name = request.POST['nam']
        contact = request.POST['con']
        Auther = request.POST['auther']
        email = request.POST['em']
        user_object = MyUser.objects.get(new_slug=slug)
        if email:
            if MyUser.objects.filter(user_email=email).exists():
                messages.warning(request, "username exists")
                return redirect('update-profile,slug')
            else:
                if name:
                    user_object.first_name = name.split(" ")[0]
                    user_object.last_name = name.split(" ")[1]
                if contact:
                    user_object.user_contact = contact
                if user_object.is_auther:
                    if Auther == 'Reader':
                        user_object.is_auther = False
                        user_object.is_active = False
                else:
                    if Auther == 'Auther':
                        user_object.is_auther = True
                        user_object.is_active = False
                if len(request.FILES) != 0:
                    image = request.FILES["im"]
                    user_object.user_image = image
                user_object.user_email = email
                user_object.save()
                messages.success(request, 'sent for admin approval')
                user_object1 = MyUser.objects.filter(is_staff=True)
                task_func.delay(message="A user wants to update there profile",
                                title="profile updation Request", receiver=[user.user_email for user in user_object1])
                return redirect('index')
        else:

            if name:
                user_object.first_name = name.split(" ")[0]
                user_object.last_name = name.split(" ")[1]
            if contact:
                user_object.user_contact = contact
            if user_object.is_auther:
                if Auther == 'Reader':
                    user_object.is_auther = False
                    user_object.is_active = False
            else:
                if Auther == 'Auther':
                    user_object.is_auther = True
                    user_object.is_active = False
            if len(request.FILES) != 0:
                image = request.FILES["im"]
                user_object.user_image = image
            user_object.save()
            messages.success(
                request, 'profile updated sent for admin approval')
            user_object1 = MyUser.objects.filter(is_staff=True)
            task_func.delay(message="A user wants to update there profile",
                            title="Profile updation request", receiver=[user.user_email for user in user_object1])
            return redirect('index')

    user_object2 = MyUser.objects.get(new_slug=slug)
    return render(request, 'account/update-profile.html', {'user_object': user_object2})
