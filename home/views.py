from django.shortcuts import redirect, render
from blog.models import Blog
from account.models import MyUser
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    p = Paginator(Blog.objects.filter(
        blog_is_approved=True).order_by('-blog_uploaded_on'), 5)
    page = request.GET.get('page')
    blog_paginate = p.get_page(page)

    return render(request, "home/index.html", {"blog_paginate": blog_paginate})


def admin(request):
    blog_object = Blog.objects.filter(
        blog_new_request=True).order_by('-blog_uploaded_on')
    user_object = MyUser.objects.filter(
        is_active=False).order_by('-sign_up_date')
    blogsdelete_object = Blog.objects.filter(
        blog_del_request=True).order_by('-blog_uploaded_on')
    return render(
        request,
        "home/admin.html",
        {"blogs_object": blog_object, "user_object": user_object,
            "blogsdelete_object": blogsdelete_object},
    )


def userapproval(request, uid):

    user_object = MyUser.objects.get(id=uid)
    user_object.is_active = True
    user_object.save()
    messages.success(request, "approved user")
    user_object = MyUser.objects.get(id=uid)
    send_mail(
        'user approval',
        'your sign up request has been approved',
        'bhattpooja471@gmail.com',
        [user_object.user_email],
        fail_silently=False,
    )
    return redirect("admin_custom")


def blogapproval(request, bid):

    blog_object = Blog.objects.get(new_slug=bid)
    blog_object.blog_is_approved = True
    blog_object.blog_new_request = False

    blog_object.save()
    messages.success(request, "approved blog")
    blog_object = Blog.objects.get(new_slug=bid)
    send_mail(
        'blog approval',
        'your blog has been approved',
        'bhattpooja471@gmail.com',
        [blog_object.blog_auther.user_email],
        fail_silently=False,
    )
    return redirect("admin_custom")


def blog_Delete_approval(request, bid):

    blog_object = Blog.objects.get(new_slug=bid)
    blog_object.delete()

    messages.success(request, "blog removed")
    blog_object = Blog.objects.get(new_slug=bid)
    send_mail(
        'blog deletion approval',
        'your blog has been deleted',
        'bhattpooja471@gmail.com',
        [blog_object.blog_auther.user_email],
        fail_silently=False,
    )
    return redirect("admin_custom")


def about(request):
    return render(request, "home/about.html")
