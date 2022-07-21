from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Blog, Comment
from account.models import MyUser
from django.core.mail import send_mail
from django.core.paginator import Paginator
# Create your views here.


def blogupload(request):
    p = Paginator(Blog.objects.filter(
        blog_is_approved=True, blog_auther=request.user.id).order_by('-blog_uploaded_on'), 5)
    page = request.GET.get('page')
    blog_paginate = p.get_page(page)
    if request.method == "POST":
        title = request.POST["tt"]
        content = request.POST["co"]

        if len(request.FILES) != 0:
            image = request.FILES["im"]
        if request.user.is_authenticated:

            blog_add = Blog(
                blog_auther=get_object_or_404(MyUser, id=request.user.id),
                blog_image=image,
                blog_content=content,
                blog_title=title,
            )
        blog_add.save()
        messages.success(request, "blog added waiting for admin approval")
        user_object = MyUser.objects.filter(is_staff=True)
        send_mail(
            "Blog Addition Request",
            "A auther wants to add a blog",
            "bhattpooja471@gmail.com",
            [user.user_email for user in user_object],
            fail_silently=False,
        )
        return redirect("index")
    return render(request, "blog/newblog.html", {"blog_paginate": blog_paginate})


def blogupdate(request, bid):
    blog_object = Blog.objects.filter(new_slug=bid)
    return render(request, "blog/updateblog.html", {"blogs": blog_object})


def blogupdate1(request):
    if request.method == "POST":
        blog_title = request.POST["tt"]
        blog_content = request.POST["co"]
        blog_id = request.POST["id1"]
        blog_object = Blog.objects.get(id=blog_id)
        if len(request.FILES) != 0:
            blog_image = request.FILES["im"]
            blog_object.blog_image = blog_image
        if request.user.is_authenticated:

            blog_object.blog_auther = get_object_or_404(
                MyUser, id=request.user.id)

            blog_object.blog_content = blog_content
            blog_object.blog_title = blog_title
            blog_object.blog_new_request = True
            blog_object.blog_is_approved = False
            blog_object.save()
            messages.success(
                request, "blog updated waiting for admin approval")
            user_object = MyUser.objects.filter(is_staff=True)
            send_mail(
                "Blog Updation Request",
                "A auther wants to update their blog",
                "bhattpooja471@gmail.com",
                [user.user_email for user in user_object],
                fail_silently=False,
            )
        return redirect(blogupload)


def blogdelete(request, bid):
    blog_object = Blog.objects.get(new_slug=bid)
    blog_object.blog_del_request = True
    blog_object.save()
    messages.success(request, "send for admin approval to delete the blog")
    user_object = MyUser.objects.filter(is_staff=True)
    send_mail(
        "Blog Deletion Request",
        "A auther wants to delete their blog",
        "bhattpooja471@gmail.com",
        [user.user_email for user in user_object],
        fail_silently=False,
    )
    return redirect(blogupload)


def open_blog(request, bid):
    blog_object = Blog.objects.filter(new_slug=bid)

    p = Paginator(Comment.objects.filter(blog_key__new_slug=bid).order_by(
        "-comment_added_on"), 7)
    page = request.GET.get('page')
    comment_paginate = p.get_page(page)
    return render(
        request,
        "blog/singleblog.html",
        {"blogs": blog_object, "comment_paginate": comment_paginate},
    )


def addcomment(request, bid):
    if request.method == "POST":
        comment_blog = request.POST["com"]
        if request.user.is_authenticated:
            blog_object = Blog.objects.get(new_slug=bid)
            comment_object = Comment(
                user=get_object_or_404(MyUser, id=request.user.id),
                blog_key=get_object_or_404(
                    Blog, id=blog_object.id),
                blog_comment=comment_blog,
            )
            comment_object.save()
            blog_object = Blog.objects.get(new_slug=bid)
            # send_mail(
            #     "Blog Comment",
            #     "your blog recived new comments",
            #     "bhattpooja471@gmail.com",
            #     [blog_object.blog_auther.user_email],
            #     fail_silently=False,
            # )
            return redirect("open_blog", bid)
        else:
            messages.warning(request, "please login")
            return redirect("signin")
