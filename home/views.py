from django.http import HttpResponse
from django.shortcuts import redirect, render
from blog.models import Blog, Search
from account.models import MyUser
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .task import task_func


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
    task_func.delay(message='your sign up request has been approved',
                    title='user approval', receiver=[user_object.user_email])

    return redirect("admin_custom")


def blogapproval(request, slug):

    blog_object = Blog.objects.get(new_slug=slug)
    blog_object.blog_is_approved = True
    blog_object.blog_new_request = False

    blog_object.save()
    messages.success(request, "approved blog")
    blog_object = Blog.objects.get(new_slug=slug)
    task_func.delay(message='your blog has been approved',
                    title='blog approval', receiver=[blog_object.blog_auther.user_email])

    return redirect("admin_custom")


def blog_Delete_approval(request, slug):

    blog_object = Blog.objects.get(new_slug=slug)
    blog_object.delete()

    messages.success(request, "blog removed")
    blog_object = Blog.objects.get(new_slug=slug)
    task_func.delay(message='your blog has been deleted',
                    title='blog deletion approval', receiver=[blog_object.blog_auther.user_email])

    return redirect("admin_custom")


def about(request):
    return render(request, 'home/about.html')


def search(request):
    if request.method == 'POST':
        search_content = request.POST['search']
    search_obj = Search.objects.filter(search_content=search_content)
    if search_obj.exists():
        return redirect('search1', search_content)
    else:
        blog = Blog.objects.filter(blog_is_approved=True)
        for i in blog:
            if search_content in i.blog_title:
                search_object = Search(
                    object_blog=i, search_content=search_content)
                search_object.save()
        return redirect('search1', search_content)


def search1(request, search):
    search_obj = Search.objects.filter(search_content=search)
    p = Paginator(search_obj, 5)
    page = request.GET.get('page')
    blog_paginate = p.get_page(page)
    if search_obj:
        return render(request, 'home/search.html', {"blog_paginate": blog_paginate})
    else:
        messages.warning(request, 'search result not found')
        return redirect('index')

