from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Blog, Comment
from account.models import MyUser
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .tasks import task_func
# Create your views here.


def blogupload(request):
    p = Paginator(Blog.objects.isapproved().filter(
        blog_auther=request.user.id), 5)
    page = request.GET.get('page')
    blog_paginate = p.get_page(page)
    if request.method == "POST":
        title = request.POST["tt"]
        content = request.POST["co"]
        blog_keyword = request.POST['key']
        blog_description = request.POST['descript']
        if len(request.FILES) != 0:
            image = request.FILES["im"]
        if request.user.is_authenticated:
            if Blog.objects.filter(blog_title=title).exists():
                messages.warning(
                    request, f'\'{title}\' already exists make your title unique')
                return redirect('addblog')
            else:
                blog_add = Blog(
                    blog_auther=get_object_or_404(MyUser, id=request.user.id),
                    blog_content=content,
                    blog_title=title,
                    blog_image=image,
                    blog_keywords=blog_keyword,
                    blog_description=blog_description,
                )
                blog_add.save()

                messages.success(
                    request, "blog added waiting for admin approval")
                user_object = MyUser.objects.isstaff()
                task_func.delay(message="An auther wants to add a blog",
                                title="Blog Addition Request", receiver=[user.user_email for user in user_object])

                return redirect("index")
    return render(request, "blog/newblog.html", {"blog_paginate": blog_paginate})


def blogupdate(request, slug):
    blog_object = Blog.objects.filter(new_slug=slug)
    return render(request, "blog/updateblog.html", {"blogs": blog_object})


def blogupdate1(request, slug):
    if request.method == "POST":
        blog_title = request.POST["tt"]
        blog_content = request.POST["co"]
        blog_keyword = request.POST['key']
        blog_description = request.POST['descript']
        blog_object = Blog.objects.get(new_slug=slug)
        if len(request.FILES) != 0:
            blog_image = request.FILES["im"]
            blog_object.blog_image = blog_image
        if request.user.is_authenticated:

            blog_object.blog_auther = get_object_or_404(
                MyUser, id=request.user.id)
            if blog_content:
                blog_object.blog_content = blog_content
            blog_object.blog_title = blog_title
            blog_object.blog_keywords = blog_keyword
            blog_object.blog_description = blog_description
            blog_object.blog_new_request = True
            blog_object.blog_is_approved = False
            blog_object.save()
            messages.success(
                request, "blog updated waiting for admin approval")
            user_object = MyUser.objects.isstaff()
            task_func.delay(message="An auther wants to update their blog",
                            title="Blog Updation Request", receiver=[user.user_email for user in user_object])

        return redirect(blogupload)


def blogdelete(request, slug):
    blog_object = Blog.objects.get(new_slug=slug)
    blog_object.blog_del_request = True
    blog_object.save()
    messages.success(request, "send for admin approval to delete the blog")
    user_object = MyUser.objects.isstaff()

    task_func.delay(message="An auther wants to delete their blog",
                    title="Blog Deletion Request", receiver=[user.user_email for user in user_object])

    return redirect(blogupload)


def open_blog(request, slug):
    blog_object = Blog.objects.filter(new_slug=slug)

    p = Paginator(Comment.objects.filter(blog_key__new_slug=slug).order_by(
        "-comment_added_on"), 7)
    page = request.GET.get('page')
    comment_paginate = p.get_page(page)
    return render(
        request,
        "blog/singleblog.html",
        {"blogs": blog_object, "comment_paginate": comment_paginate},
    )


def addcomment(request, slug):
    if request.method == "POST":
        comment_blog = request.POST["com"]
        if request.user.is_authenticated:
            blog_object = Blog.objects.get(new_slug=slug)
            comment_object = Comment(
                user=get_object_or_404(MyUser, id=request.user.id),
                blog_key=get_object_or_404(
                    Blog, id=blog_object.id),
                blog_comment=comment_blog,
            )
            comment_object.save()
            blog_object = Blog.objects.get(new_slug=slug)

            return redirect("open-blog", slug)
        else:
            messages.warning(request, "please login")
            return redirect("sign-in")
